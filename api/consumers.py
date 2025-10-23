# api/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RequeteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("requetes_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("requetes_group", self.channel_name)

    async def send_requete_update(self, event):
    # envoie tout l'event, pas seulement les données
        await self.send(text_data=json.dumps(event))

