from django.urls import path
from . import views

app_name = "stories"
urlpatterns = [
	path("create/",views.AddStory.as_view(),name="add_story"),
]