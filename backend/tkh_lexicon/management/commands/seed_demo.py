from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from tkh_lexicon.models import Technique
from tkh_patterns.models import Tul


class Command(BaseCommand):
    help = "Seed demo data: techniques, tuls, demo user"

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="demo").exists():
            User.objects.create_user(username="demo", password="demo123")
            self.stdout.write(self.style.SUCCESS("Created user demo/demo123"))

        techniques = [
            {
                "names": {"pl": "Ap Chagi", "en": "Front Kick", "kr": "앞차기"},
                "category": "kick",
                "min_belt": 7,
                "key_points": ["prostuj kolano"],
                "common_mistakes": ["niski naskok"],
                "videos": {"front": "https://example.com/front.mp4"},
                "tags": ["fundamentals"],
            },
            {
                "names": {"pl": "Yop Chagi", "en": "Side Kick", "kr": "옆차기"},
                "category": "kick",
                "min_belt": 7,
                "key_points": ["biodro równolegle"],
                "common_mistakes": ["otwarte biodro"],
                "videos": {"front": "https://example.com/side.mp4"},
                "tags": ["fundamentals"],
            },
        ]
        for t in techniques:
            Technique.objects.get_or_create(
                category=t["category"],
                names=t["names"],
                defaults={
                    "min_belt": t["min_belt"],
                    "key_points": t["key_points"],
                    "common_mistakes": t["common_mistakes"],
                    "videos": t["videos"],
                    "tags": t["tags"],
                },
            )

        tuls = [
            {"name": "Chon-Ji", "belt": 9, "steps": ["s1", "s2"], "videos": {"demo": "https://example.com/chonji.mp4"}},
            {"name": "Dan-Gun", "belt": 8, "steps": ["s1", "s2"], "videos": {"demo": "https://example.com/dangun.mp4"}},
        ]
        for x in tuls:
            Tul.objects.get_or_create(
                name=x["name"],
                defaults={
                    "belt": x["belt"],
                    "steps": x["steps"],
                    "videos": x["videos"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Seed completed"))

