from rest_framework import serializers
from .models import Requete

class RequeteSerializer(serializers.ModelSerializer):
    utilisateurNom = serializers.CharField(source="utilisateur.username", read_only=True)
    utilisateurId = serializers.IntegerField(source="utilisateur.id", read_only=True)

    class Meta:
        model = Requete
        fields = ["id", "utilisateurId", "utilisateurNom", "destination", "date", "etat", "message"]
