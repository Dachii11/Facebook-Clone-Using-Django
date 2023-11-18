from django.urls import path
from . import views

app_name = "marketplace"
urlpatterns = [
	path("",views.Marketplace.as_view(),name='marketplace'),
	path("search/",views.Search.as_view(),name="search"),
	path("add/",views.AddProduct.as_view(),name="add_product"),
	path("<str:pk>/",views.ProductDetail.as_view(),name='detail'),
]