from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account
from mimetypes import guess_type
from django.utils import timezone
import datetime

class Story(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE)
	file = models.FileField(upload_to="Stories",blank=True)
	views = models.ManyToManyField(Account,related_name="story_views")
	time = models.DateTimeField(auto_now_add=True)

	def media_type_html(self):
		type_tuple = guess_type(self.file.url, strict=True)
		if (type_tuple[0]).__contains__("image"):
			return "image"
		elif (type_tuple[0]).__contains__("video"):
			return "video"

	class Meta:
		ordering = ['-time']