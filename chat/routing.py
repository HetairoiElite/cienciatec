# chat/routing.py
if __name__ == '__main__':
    import django
    django.setup()

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/thread/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]