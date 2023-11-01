from django.shortcuts import render,redirect
from .models import *
from django.views.generic.base import View
from operator import attrgetter
from accounts.models import Account,Group
from django.contrib.auth.models import User
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def CreatePostNotification(user,post):
	PostNotifications.objects.create(user=user,post=post).save() 

def CreateSharedPostNotification(user,shared_post,post):
	SharedPostNotifications.objects.create(user=user,shared_post=shared_post,post=post).save()
	
def CreateCommentNotification(user,comment):
	CommentNotifications.objects.create(user=user,post_comment=comment).save()

def CreateReplyCommentNotification(user,comment,reply_comment):
	ReplyCommentNotifications.objects.create(user=user,comment=comment,repylied_comment=reply_comment).save()

@method_decorator(login_required,name='dispatch')
class Notifications(View):
	template_name = "notifications/index.html"
	def get(self,request,*args,**kwargs):
		my_profile = Account.objects.get(user=User.objects.get(id=request.user.id))
		notifications = []
		filtered_nots = []
		notifications.extend(PostNotifications.objects.all())
		notifications.extend(CommentNotifications.objects.all())
		notifications.extend(ReplyCommentNotifications.objects.all())
		notifications.extend(SharedPostNotifications.objects.all())
		for i in range(len(notifications)):
			if User.objects.get(id=notifications[i].user.user.id) in my_profile.friends.all():
				filtered_nots.append(notifications[i])
		filtered_nots.extend(GroupInviteNotifications.objects.filter(receiver=Account.objects.get(user=request.user)))
		for i in filtered_nots:
			i.seen=True
			i.save()
		filtered_nots.sort(key=attrgetter("date"))
		count_new_msgs = len(Message.objects.filter(to_user=my_profile,seen=False))
		context = {"notifications":reversed(filtered_nots),"my_profile":my_profile,
					"count_new_msgs":count_new_msgs,"new_notifications":new_notification_counter(my_profile.id)}
		return render(request,self.template_name,context)

	def post(self,request,*args,**kwargs):
		print(request.POST)
		user = Account.objects.get(user=request.user)
		if "theme" in request.POST:
			if user.theme==True: user.theme=False
			else: user.theme=True
			user.save()	
			return redirect(request.META["HTTP_REFERER"])
		else:
			# Check if user changed input data in html form
			try:
				group = Group.objects.get(id=request.POST["accept"])
				receiver = Account.objects.get(id=request.POST["ud"])
				if receiver!=user:
					print("Malicious Attempt!")
					return redirect(request.META["HTTP_REFERER"])
				if GroupInviteNotifications.objects.filter(group_to_invite=group,receiver=receiver).exists():
					group.members.add(receiver)
					group.save()
					GroupInviteNotifications.objects.filter(group_to_invite=group,receiver=receiver).delete()
			except:
				raise "Malicious Attempt!"
		return redirect(request.META["HTTP_REFERER"])
		
def new_notification_counter(my_profile):
	notifications=[]
	my_profile = Account.objects.get(id=my_profile)
	friends = [Account.objects.get(user=friend) for friend in my_profile.friends.all()]
	for friend in friends:
		if PostNotifications.objects.filter(user=friend,seen=False).exists():
			notifications.extend(PostNotifications.objects.filter(user=friend,seen=False))
		elif SharedPostNotifications.objects.filter(user=friend,seen=False).exists():
			notifications.extend(SharedPostNotifications.objects.filter(user=friend,seen=False))
		elif CommentNotifications.objects.filter(user=friend,seen=False).exists():
			notifications.extend(CommentNotifications.objects.filter(user=friend,seen=False))
		elif ReplyCommentNotifications.objects.filter(user=friend,seen=False).exists():
			notifications.extend(ReplyCommentNotifications.objects.filter(user=friend,seen=False))
		
	if GroupInviteNotifications.objects.filter(receiver=my_profile,seen=False).exists():
		notifications.extend(GroupInviteNotifications.objects.filter(receiver=my_profile,seen=False))
	return len(notifications)
