from django.db import models

class ClinicalTrial(models.Model):
    trial_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=500)
    disease = models.CharField(max_length=255)
    phase = models.CharField(max_length=50)
    status = models.CharField(max_length=100)

class TrialDocument(models.Model):
    trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)