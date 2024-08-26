from django.db import models
from leads.models import Lead

class Appointment(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    confirmed = models.BooleanField(default=False)
    