from django.contrib import admin
from .models import Tul
from django import forms
from django_json_widget.widgets import JSONEditorWidget


class TulForm(forms.ModelForm):
    class Meta:
        model = Tul
        fields = "__all__"
        widgets = {
            "steps": JSONEditorWidget(options={"mode": "tree"}),
            "tempo": JSONEditorWidget(options={"mode": "tree"}),
            "videos": JSONEditorWidget(options={"mode": "tree"}),
        }


@admin.register(Tul)
class TulAdmin(admin.ModelAdmin):
    form = TulForm
    list_display = ("id", "name", "belt", "is_draft", "updated_at")
    list_filter = ("belt", "is_draft")
    search_fields = ("name",)

# Register your models here.
