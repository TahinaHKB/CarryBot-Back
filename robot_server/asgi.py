import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import path
from api.consumers import RequeteConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'robot_server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/requetes/", RequeteConsumer.as_asgi()),
        ])
    ),
})
