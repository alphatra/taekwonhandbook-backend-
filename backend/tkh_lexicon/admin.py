from django import forms
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from .models import Technique


class TechniqueForm(forms.ModelForm):
    class Meta:
        model = Technique
        fields = "__all__"
        widgets = {
            "names": JSONEditorWidget(options={"mode": "tree"}),
            "key_points": JSONEditorWidget(options={"mode": "tree"}),
            "common_mistakes": JSONEditorWidget(options={"mode": "tree"}),
            "videos": JSONEditorWidget(options={"mode": "tree"}),
            "tags": JSONEditorWidget(options={"mode": "tree"}),
        }


@admin.register(Technique)
class TechniqueAdmin(admin.ModelAdmin):
    form = TechniqueForm
    list_display = ("id", "category", "min_belt", "is_draft", "updated_at")
    list_filter = ("category", "min_belt", "is_draft")
    search_fields = ("names", "tags")

# Register your models here.
