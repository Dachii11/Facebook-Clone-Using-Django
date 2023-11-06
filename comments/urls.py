from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
	path("<str:pk>/",views.ReplyComment.as_view(),name='reply_comment'),
	path("report-comment/<str:pk>/",views.ReportComment.as_view(),name="report_comment"),
]