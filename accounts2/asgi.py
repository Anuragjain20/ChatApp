"""
ASGI config for accounts2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from main.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounts2.settings')

application = get_asgi_application()
ws_patterns = [
    path('rooms/<room_name>/',ChatConsumer),
]


application = ProtocolTypeRouter({
    'websocket': URLRouter(ws_patterns)
})

