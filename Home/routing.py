from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/user_(?P<user_id>\d+)/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r"ws/(?P<roomName>[^/]+)/$", consumers.ChatConsumer.as_asgi()),
]


