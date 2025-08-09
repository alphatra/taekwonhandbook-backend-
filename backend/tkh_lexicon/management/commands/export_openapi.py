from django.core.management.base import BaseCommand
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.renderers import OpenApiJsonRenderer


class Command(BaseCommand):
    help = "Export OpenAPI schema to stdout as JSON"

    def handle(self, *args, **options):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=None, public=True)
        data = OpenApiJsonRenderer().render(schema, renderer_context={})
        self.stdout.write(data.decode("utf-8"))

