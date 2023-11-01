from chat import consumers
from django.urls import re_path

websocket_urlpatterns = [
	re_path(r"ws/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
	re_path(r"ws/search/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
]
