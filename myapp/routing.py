from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<thread_id>\w+)/$', consumers.MessageConsumer.as_asgi()),
]
