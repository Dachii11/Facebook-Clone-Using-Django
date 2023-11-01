import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import chat.routing
import mainApp.routing
import accounts.routing
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fb.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
	"http":get_asgi_application(),
	"websocket":AllowedHostsOriginValidator(
		AuthMiddlewareStack(URLRouter([
				*chat.routing.websocket_urlpatterns,
				*mainApp.routing.websocket_urlpatterns,
				*accounts.routing.websocket_urlpatterns,
			])
		)
	)
})

