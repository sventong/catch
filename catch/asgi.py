"""
ASGI config for catch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

# from app.consumers import GameConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catch.settings')

django_asgi_app = get_asgi_application()

from app.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http':django_asgi_app,
    'websocket':AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    
})

