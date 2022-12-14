"""
ASGI config for cienciatec project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import chat.routing
import os


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cienciatec.settings')

django_asgi_app = get_asgi_application()

from chat.consumers import ChatConsumer


application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(
                [
                re_path(r"ws/chat/thread/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
                ]
            ))
        ),
    }
)
