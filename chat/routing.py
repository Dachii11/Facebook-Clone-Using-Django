from django.urls import path
from . import consumers
from django.urls import re_path
websocket_urlpatterns = [
	re_path(r"ws/chat/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
	re_path(r"ws/chat/group/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
	re_path(r"ws/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
]
