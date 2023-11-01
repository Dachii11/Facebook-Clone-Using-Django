from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
	path("",views.Notifications.as_view(),name="notifications"),	
]