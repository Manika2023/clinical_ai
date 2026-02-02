from django.contrib import admin
from .models import ClinicalTrial, TrialDocument


@admin.register(ClinicalTrial)
class ClinicalTrialAdmin(admin.ModelAdmin):
    list_display = ("trial_id", "title", "disease", "phase", "status")
    search_fields = ("trial_id", "title", "disease")
    list_filter = ("phase", "status")
    ordering = ("trial_id",)


@admin.register(TrialDocument)
class TrialDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "trial", "uploaded_at")
    search_fields = ("title", "content", "trial__trial_id")
    list_filter = ("uploaded_at",)
    autocomplete_fields = ("trial",)
