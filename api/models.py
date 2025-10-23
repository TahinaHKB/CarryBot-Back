from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

class Requete(models.Model):
    ETAT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('arriver', 'Arrivé'),
        ('confirme', 'Confirmé'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='en_attente')
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.utilisateur.username} -> {self.destination} ({self.etat})"
