from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin,DetailView
from comments.models import Comment,CommentReply
from accounts.views import ProfileAccountMixin
from accounts.models import Account
from mainApp.views import PostMixins
from notifications.models import ReplyCommentNotifications
from notifications.views import CreateReplyCommentNotification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required,name='dispatch')
class ReplyComment(ProfileAccountMixin,SingleObjectMixin,View):
	model = Comment

	def get(self,request,*args,**kwargs):
		self.object = self.get_object()
		comment = self.get_context_data(object=self.object)
		return render(request,"comments/reply_comment.html",comment)

	def post(self,request,*args,**kwargs):
		if "text" in request.POST:
			parrent_comment = Comment.objects.get(id=request.POST["comment_id"])
			user = Account.objects.get(user=request.user)
			rep = CommentReply.objects.create(text=request.POST["text"],parrent_comment=parrent_comment,user=user)
			rep.save()
			CreateReplyCommentNotification(user,parrent_comment,rep)
		if "reply_like" in request.POST:
			reply_comm = CommentReply.objects.get(id=request.POST["comment"])
			if Account.objects.get(user=request.user) in reply_comm.likes.all():
				reply_comm.likes.remove(Account.objects.get(user=request.user))
			else:
				reply_comm.likes.add(Account.objects.get(user=request.user))
		
		if "like" in request.POST:
			comment = Comment.objects.get(id=request.POST["comment"],type_of_comment=request.POST["type_of_comment"])
			if Account.objects.get(user=request.user) in comment.likes.all():
				comment.likes.remove(Account.objects.get(user=request.user))
			else:
				comment.likes.add(Account.objects.get(user=request.user))
		
		return redirect(request.META["HTTP_REFERER"])

