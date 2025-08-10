from __future__ import annotations

from typing import Iterable, List

from django.conf import settings
from django.core.management.base import BaseCommand

try:
    import meilisearch  # type: ignore
except Exception:  # pragma: no cover
    meilisearch = None


def chunked(iterable: Iterable, size: int) -> Iterable[List]:
    batch: List = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


class Command(BaseCommand):
    help = "Reindex Meilisearch indices for techniques and tuls (supports --dry-run)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--types",
            default="techniques,tuls",
            help="Comma-separated list: techniques,tuls",
        )
        parser.add_argument("--batch-size", type=int, default=500)
        parser.add_argument("--drop", action="store_true")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        types = [t.strip() for t in str(options["types"]).split(",") if t.strip()]
        batch_size = int(options["batch_size"]) or 500
        drop = bool(options["drop"])
        dry_run = bool(options["dry_run"])

        if dry_run:
            self.stdout.write(self.style.WARNING("Running in DRY-RUN mode (no writes)."))

        # Import models lazily to avoid circulars
        from tkh_lexicon.models import Technique
        from tkh_patterns.models import Tul

        # Prepare data builders
        def iter_techniques():
            for t in Technique.objects.all().iterator(chunk_size=batch_size):
                yield {
                    "id": t.id,
                    "names": getattr(t, "names", {}),
                    "category": getattr(t, "category", ""),
                    "min_belt": getattr(t, "min_belt", None),
                }

        def iter_tuls():
            for x in Tul.objects.all().iterator(chunk_size=batch_size):
                yield {
                    "id": x.id,
                    "name": getattr(x, "name", ""),
                    "belt": getattr(x, "belt", None),
                }

        total = {"techniques": 0, "tuls": 0}

        # Count only
        if "techniques" in types:
            total["techniques"] = Technique.objects.count()
        if "tuls" in types:
            total["tuls"] = Tul.objects.count()

        self.stdout.write(f"Totals → techniques={total['techniques']} tuls={total['tuls']}")

        if dry_run:
            return

        if not meilisearch or not getattr(settings, "MEILISEARCH_URL", None):
            self.stdout.write(self.style.ERROR("Meilisearch not available or MEILISEARCH_URL not set"))
            return

        client = meilisearch.Client(settings.MEILISEARCH_URL, getattr(settings, "MEILISEARCH_API_KEY", "") or None)

        if "techniques" in types:
            idx_t = client.index("techniques")
            if drop:
                try:
                    client.delete_index("techniques")
                except Exception:
                    pass
                idx_t = client.index("techniques")
            # Settings
            try:
                idx_t.update_searchable_attributes(["names", "category"]).wait()
                idx_t.update_filterable_attributes(["min_belt", "category"]).wait()
                idx_t.update_displayed_attributes(["id", "names", "category", "min_belt"]).wait()
            except Exception:
                pass
            # Data
            for batch in chunked(iter_techniques(), batch_size):
                idx_t.add_documents(batch, primary_key="id")
            self.stdout.write(self.style.SUCCESS(f"Indexed techniques: {total['techniques']}"))

        if "tuls" in types:
            idx_u = client.index("tuls")
            if drop:
                try:
                    client.delete_index("tuls")
                except Exception:
                    pass
                idx_u = client.index("tuls")
            try:
                idx_u.update_searchable_attributes(["name"]).wait()
                idx_u.update_filterable_attributes(["belt"]).wait()
                idx_u.update_displayed_attributes(["id", "name", "belt"]).wait()
            except Exception:
                pass
            for batch in chunked(iter_tuls(), batch_size):
                idx_u.add_documents(batch, primary_key="id")
            self.stdout.write(self.style.SUCCESS(f"Indexed tuls: {total['tuls']}"))

