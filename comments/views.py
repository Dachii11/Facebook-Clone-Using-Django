from django.shortcuts import render,redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin,DetailView
from comments.models import Comment,CommentReply,CommentReport
from accounts.views import ProfileAccountMixin
from accounts.models import Account
from mainApp.views import PostMixins
from notifications.models import ReplyCommentNotifications
from django.views.generic.edit import CreateView
from notifications.views import CreateReplyCommentNotification
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.views import AccountMixin
from django.urls import reverse_lazy

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


class ReportComment(CreateView):
	template_name = "comments/report_comment.html"
	model = CommentReport
	fields = ("reason","text")

	def get_context_data(self,*args,**kwargs):
		context = super(ReportComment,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=self.request.user)
		return context

	def form_valid(self,form):
		form.instance.comment = Comment.objects.get(id=self.request.get_full_path().split("/")[3])
		form.instance.user_who_reports = Account.objects.get(user=self.request.user)
		form.save()
		return super(ReportComment,self).form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy("mainApp:index")
