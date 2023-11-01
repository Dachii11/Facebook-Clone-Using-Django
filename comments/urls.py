from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
	path("<str:pk>/",views.ReplyComment.as_view(),name='reply_comment'),
]