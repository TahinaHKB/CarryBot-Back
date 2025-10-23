from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from api import consumers  # ton app API

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/requetes/", consumers.RequeteConsumer.as_asgi()),
        ])
    ),
})
