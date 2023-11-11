from django.shortcuts import render,redirect
from .forms import AddStoryForm
from django.views.generic.edit import FormView
from .models import Story
from accounts.models import Account
from accounts.views import SettingsMixin,RemoveFile
from django.urls import reverse_lazy
from django.contrib.auth.models import User
import datetime,timespan
from django.contrib import messages
from django.db.models.functions import Now
import threading
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
@method_decorator(login_required,name='dispatch')
class AddStory(FormView):
	model = Story
	form_class = AddStoryForm
	template_name = "stories/add_story.html"

	CONTENT_TYPES = ["image","video"]
	MAX_LIMIT_SIZE = 20971520

	def form_valid(self,form):
		form.instance.user = Account.objects.get(user=self.request.user)
		print(form.cleaned_data["file"].size)
		if form.cleaned_data["file"].size>self.MAX_LIMIT_SIZE:
			messages.error(self.request,"File is too large. Maximum 20MB")
			return redirect(self.request.META["HTTP_REFERER"])
		else:
			form.save()
		return super(AddStory,self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(AddStory,self).get_context_data(**kwargs)
		context["my_profile"]=Account.objects.get(user=self.request.user)
		return context
		
	def get_success_url(self):
		return reverse_lazy("mainApp:index")

def delete_old_stories():
	threading.Timer(10.0,delete_old_stories).start()    
	stories = Story.objects.filter(time__lt=Now()-datetime.timedelta(days=1))
	if stories:
		for story in stories:
			remove = RemoveFile(story.file.url)
			remove.remove_file()
			story.delete()
			
delete_old_stories()
