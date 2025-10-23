from django.contrib import admin
from .models import Requete

@admin.register(Requete)
class RequeteAdmin(admin.ModelAdmin):
    list_display = ('id', 'utilisateur', 'destination', 'etat', 'date')  # colonnes visibles dans la liste
    list_filter = ('etat', 'date')  # filtres sur la droite
    search_fields = ('utilisateur__username', 'destination', 'message')  # barre de recherche
    ordering = ('-date',)  # tri par date décroissante
