from django.contrib import admin
from django import forms
from django_json_widget.widgets import JSONEditorWidget
from .models import ExamSyllabus


class ExamSyllabusForm(forms.ModelForm):
    class Meta:
        model = ExamSyllabus
        fields = "__all__"
        widgets = {
            "strength_tests": JSONEditorWidget(options={"mode": "tree"}),
            "theory_qs": JSONEditorWidget(options={"mode": "tree"}),
        }


@admin.register(ExamSyllabus)
class ExamSyllabusAdmin(admin.ModelAdmin):
    form = ExamSyllabusForm
    list_display = ("belt", "is_draft", "updated_at")
    list_filter = ("belt", "is_draft")

# Register your models here.
