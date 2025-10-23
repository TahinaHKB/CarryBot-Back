from rest_framework import viewsets
from .models import Requete
from .serializers import RequeteSerializer
from .permissions import IsWpfOrAuthenticated
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions

class ListeRequetesView(APIView):
    permission_classes = [IsAuthenticated]  # token requis ✅

    def get(self, request):
        requetes = Requete.objects.filter(utilisateur=request.user).order_by('-date')
        serializer = RequeteSerializer(requetes, many=True)
        return Response(serializer.data)
    
class RequeteDeleteAPIView(generics.DestroyAPIView):
    queryset = Requete.objects.all()
    serializer_class = RequeteSerializer
    permission_classes = [permissions.IsAuthenticated]

    # optionnel : ne permettre que la suppression par l'utilisateur propriétaire
    def get_object(self):
        obj = super().get_object()
        if obj.utilisateur != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas supprimer cette requête")
        return obj

class ConfirmerRequeteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # ou AllowAny si tu veux pas protéger

    def post(self, request, pk):
        try:
            requete = Requete.objects.get(id=pk)
        except Requete.DoesNotExist:
            return Response({"error": "Requête non trouvée"}, status=status.HTTP_404_NOT_FOUND)
        
        # Mettre à jour l'état
        requete.etat = "confirme"
        requete.save()

        serializer = RequeteSerializer(requete)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all()
    serializer_class = RequeteSerializer
    permission_classes = [IsWpfOrAuthenticated]

    def perform_create(self, serializer):
        # Sauvegarde l'instance
        instance = serializer.save(utilisateur=self.request.user)

        # Envoi au groupe WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "requetes_group",
            {
                "type": "send_requete_update",
                "data": {
                    "id": instance.id,
                    "utilisateurNom": instance.utilisateur.username,
                    "destination": instance.destination,
                    "etat": instance.etat,
                    "date" : instance.date,
                    "message": instance.message
                }
            }
        )

class SignupView(APIView):
    def post(self, request):
        nom = request.data.get("nom")
        prenom = request.data.get("prenom")
        email = request.data.get("email")
        mot_de_passe = request.data.get("mot_de_passe")

        # Vérification de base
        if not all([nom, prenom, email, mot_de_passe]):
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Cet email est déjà utilisé."}, status=status.HTTP_400_BAD_REQUEST)

        # Création de l'utilisateur
        user = User.objects.create(
            username=email,
            first_name=prenom,
            last_name=nom,
            email=email,
            password=make_password(mot_de_passe)
        )

        return Response({"message": "Compte créé avec succès"}, status=status.HTTP_201_CREATED)

class CreerRequeteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RequeteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(utilisateur=request.user) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)