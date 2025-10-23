# api/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Requete
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import RequeteSerializer

channel_layer = get_channel_layer()

@receiver(post_save, sender=Requete)
def requete_created_or_updated(sender, instance, created, **kwargs):
    data = RequeteSerializer(instance).data
    event_type = "create" if created else "update"
    async_to_sync(channel_layer.group_send)(
        "requetes_group",
        {
            "type": "send_requete_update",
            "event": event_type,
            "data": data
        }
    )

@receiver(post_delete, sender=Requete)
def requete_deleted(sender, instance, **kwargs):
    data = {"id": instance.id}
    async_to_sync(channel_layer.group_send)(
        "requetes_group",
        {
            "type": "send_requete_update",
            "event": "delete",
            "data": data
        }
    )
