from django.urls import path, include
from rest_framework import routers
from .views import ConfirmerRequeteAPIView, CreerRequeteView, RequeteDeleteAPIView, RequeteViewSet, SignupView, ListeRequetesView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'requetes', RequeteViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Authentification JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inscription
    path('signup/', SignupView.as_view(), name='signup'),
    path('requete/creer/', CreerRequeteView.as_view(), name='creer_requete'),
    path('requete/liste/', ListeRequetesView.as_view(), name='liste-requetes'),
    path("requete/<int:pk>/delete/", RequeteDeleteAPIView.as_view(), name="requete-delete"),
    path('requete/<int:pk>/confirmer/', ConfirmerRequeteAPIView.as_view(), name='confirmer-requete'),
]
