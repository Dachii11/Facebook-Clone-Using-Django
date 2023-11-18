from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Sell
from accounts.models import Account
from django.contrib.auth.models import User
from django.views.generic.detail import SingleObjectMixin,DetailView
from django.views.generic.edit import FormView,CreateView
from notifications.views import new_notification_counter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.db.models import F,Q
from .forms import AddProductForm
from chat.models import Message

class MarketplaceMixin(object):
	def post(self,request,*args,**kwargs):
		if "accessories" in request.POST:
			sells = Sell.objects.filter(category="Apperal & Accessories")
		elif "arts" in request.POST:
			sells = Sell.objects.filter(category="Arts & Entertainment")
		elif "foods" in request.POST:
			sells = Sell.objects.filter(category="Food & Beverages")
		elif "furniture" in request.POST:
			sells = Sell.objects.filter(category="Furniture")
		elif "bussiness" in request.POST:
			sells = Sell.objects.filter(category="Business & Industrial Products")
		elif "camera" in request.POST:
			sells = Sell.objects.filter(category="Camera & equipment's")
		elif "garden" in request.POST:
			sells = Sell.objects.filter(category="Home & Garden")
		elif "bags" in request.POST:
			sells = Sell.objects.filter(category="Luggage & Bags")
		elif "toys" in request.POST:
			sells = Sell.objects.filter(category="Toys and Games")
		elif "vehicles" in request.POST:
			sells = Sell.objects.filter(category="Vehicles & Spare Parts")
		elif "software" in request.POST:
			sells = Sell.objects.filter(category="Software & Hardware")
		elif "sport" in request.POST:
			sells = Sell.objects.filter(category="Sporting goods")
		elif "baby" in request.POST:
			sells = Sell.objects.filter(category="Baby Products")
		elif "electronics" in request.POST:
			sells = Sell.objects.filter(category="Electronics")
		elif "health" in request.POST:
			sells = Sell.objects.filter(category="Health & Beauty Products")
		elif "office" in request.POST:
			sells = Sell.objects.filter(category="Office Supplies")
		else:
			sells = Sell.objects.all()
			
		try:
			category = sells[0].category
		except IndexError:
			category = "Not Found"

		my_profile = Account.objects.get(user=request.user)
		l,c = get_notifications_data(my_profile)
		return render(request,"marketplace/index.html",{"sells":sells,"my_profile":my_profile,"category":category,"count_new_msgs":l,"new_notifications":c})

@method_decorator(login_required,name='dispatch')
class Search(MarketplaceMixin,ListView):
	template_name = "marketplace/index.html"

	def get(self,request,*args,**kwargs):
		query = self.request.GET.get('q')
		products = Sell.objects.filter(Q(name__icontains=query))
		my_profile = Account.objects.get(user=self.request.user)
		l,c = get_notifications_data(my_profile)
		return render(self.request,self.template_name,{
			"count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False)),
			"sells":products,"my_profile":Account.objects.get(user=self.request.user),
			"count_new_msgs":l,"new_notifications":c,
			})

@method_decorator(login_required,name='dispatch')
class Marketplace(MarketplaceMixin,ListView):
	model = Sell
	template_name = "marketplace/index.html"
	context_object_name = 'sells'

	def get_context_data(self,*args,**kwargs):
		context = super(Marketplace,self).get_context_data(**kwargs)
		context["my_profile"]=Account.objects.get(user=self.request.user)
		l,c = get_notifications_data(context["my_profile"])
		context["count_new_msgs"] = l
		context["new_notifications"] = c
		return context

@method_decorator(login_required,name='dispatch')
class ProductDetail(MarketplaceMixin,DetailView):
	model = Sell
	template_name = "marketplace/product_detail.html"
	context_object_name = "product"

	def get(self,request,*args,**kwargs):
		product = Sell.objects.get(id=self.request.get_full_path().split('/')[2])
		user = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		if user not in product.total_views.all():
			product.total_views.add(user)
		return render(request,self.template_name,{"product":product,"my_profile":user})

class AddProduct(FormView):
	model = Sell
	form_class = AddProductForm
	template_name = "marketplace/addproduct.html"

	def form_valid(self,form):
		print(True)
		form.instance.seller = Account.objects.get(user=self.request.user)
		form.save()
		return super(AddProduct,self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy("marketplace:marketplace")
			
	 
def get_notifications_data(account):
	l = len(Message.objects.filter(to_user=account,seen=False))
	count = new_notification_counter(account.id)
	return l,count