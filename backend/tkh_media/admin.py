from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django_json_widget.widgets import JSONEditorWidget
from .models import MediaAsset


class MediaAssetForm(forms.ModelForm):
    class Meta:
        model = MediaAsset
        fields = "__all__"
        widgets = {
            "resolutions": JSONEditorWidget(options={"mode": "tree"}),
            "thumbnails": JSONEditorWidget(options={"mode": "tree"}),
            "meta": JSONEditorWidget(options={"mode": "tree"}),
        }


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    form = MediaAssetForm
    list_display = ("id", "thumb", "kind", "file", "status", "updated_at")
    list_filter = ("kind", "status")
    search_fields = ("file",)
    filter_horizontal = ("techniques", "tuls")

    def thumb(self, obj):
        if obj.thumbnails:
            url = obj.thumbnails[0]
            # jeśli używasz S3/MinIO + CDN, można zbudować pełny URL tutaj
            return mark_safe(f'<img src="{url}" alt="thumb" style="height:40px; object-fit:cover;"/>')
        return "—"
    thumb.short_description = "Podgląd"

# Register your models here.
