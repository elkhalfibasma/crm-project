from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    STATUS_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('contacté', 'Contacté'),
        ('converti', 'Converti'),
        ('perdu', 'Perdu'),
    ]
    SOURCE_CHOICES = [
        ('Site Web', 'Site Web'),
        ('Publicité', 'Publicité'),
        ('Référence', 'Référence'),
        ('Autre', 'Autre'),
    ]

    Prénom = models.CharField(max_length=100)
    Nom = models.CharField(max_length=100)
    Email = models.EmailField()
    Télephone = models.CharField(max_length=20)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    crée = models.DateTimeField(auto_now_add=True)
    Assigné = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')

    def __str__(self):
        return f"{self.Prénom} {self.Nom}"
