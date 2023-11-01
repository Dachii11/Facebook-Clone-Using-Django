from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
	re_path(r"ws/accounts/profile/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
	re_path(r"ws/accounts/(?P<chat>\w+)/$",consumers.ChatConsumer.as_asgi()),
]
