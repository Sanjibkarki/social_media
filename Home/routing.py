from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<roomName>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
]