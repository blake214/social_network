"""
ASGI config for social_network project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import myapp.routing
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            myapp.routing.websocket_urlpatterns
        )
    ),
})

'''
NOTE: Personal notes in running the asgi part of the application
Redis is a system package, so it doesnt need to run within the python enviroment

To check if redis is running:
- ps aux | grep redis-server (this shows the port)
- redis-cli ping (this is one way)

You can try shutdown redis with:
- redis-cli (This starts the shell)
- SHUTDOWN (from within the shell)

Start redis with:
- redis-start
'''
