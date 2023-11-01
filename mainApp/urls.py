from django.urls import path
from . import views

app_name = 'mainApp'
urlpatterns = [
	path("home/",views.Home.as_view(),name='index'),
	path("search/",views.Search.as_view(),name="search"),
	path("report/",views.Report.as_view(),name="report"),
	path("help/",views.Help.as_view(),name="help"),
	path("feelings/",views.FeelingsStatus.as_view(),name="feelings"),
]