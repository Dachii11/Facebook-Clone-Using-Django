from django.db import models
from accounts.models import Account

class Sell(models.Model):
	categories = (
		("Apperal & Accessories","Apperal & Accessories"),
		("Arts & Entertainment","Arts & Entertainment"),
		("Food & Beverages","Food & Beverages"),
		("Furniture","Furniture"),
		("Business & Industrial Products","Business & Industrial Products"),
		("Camera & equipment's","Camera & equipment's"),
		("Home & Garden","Home & Garden"),
		("Luggage & Bags","Luggage & Bags"),
		("Toys and Games","Toys and Games"),
		("Vehicles & Spare Parts","Vehicles & Spare Parts"),
		("Software & Hardware","Software & Hardware"),
		("Sporting goods","Sporting goods"),
		("Baby Products","Baby Products"),
		("Electronics","Electronics"),
		("Health & Beauty Products","Health & Beauty Products"),
		("Office Supplies","Office Supplies"),
	)
	seller = models.ForeignKey(Account,on_delete=models.CASCADE)
	name = models.CharField(max_length=250,null=True)
	image = models.ImageField(upload_to='sell')
	category = models.CharField(choices=categories,max_length=40,null=True)
	price = models.FloatField(default=0.0,null=True)
	description = models.TextField(max_length=1000,null=True,blank=True)
	uploaded = models.DateTimeField(auto_now_add=True)
	total_views = models.ManyToManyField(Account,related_name="total_views")

	def __str__(self):
		return self.name[:50]