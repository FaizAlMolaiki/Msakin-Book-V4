from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

# from chat.routing import websocket_urlpatterns as chat_ws_urls
from notifications.routing import websocket_urlpatterns as notifiations_ws_urls
from properties.routing import websocket_urlpatterns as properties_ws_urls

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                # chat_ws_urls+
                notifiations_ws_urls+
                properties_ws_urls

            )
        )
    ),
})