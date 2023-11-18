from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.base import View
from posts.models import Post,SharePost,SavedPosts
from accounts.models import GroupPost,GroupSharePost,Account,FriendRequest,Group,GroupVisitors
from django.contrib.auth.models import User
from chat.models import Message
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from comments.models import Comment,CommentReply
from operator import attrgetter
from django.db.models import Q
from .models import Feelings,ShareFeelingsPosts
from chat.models import PrivateChat
from notifications.models import PostNotifications
from notifications.views import *
from .forms import FeelingsForm
from stories.models import Story
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

class PostMixins(object):
	def post(self,request,*args,**kwargs):
		user = Account.objects.get(user=request.user)
		if "text" in request.POST:
			text = request.POST['text']
			post_id = request.POST['post_id']
			type_of_post = request.POST["type_of_post"]
			print(type_of_post)
			if type_of_post == "post":
				comment = Comment.objects.create(user=user,type_of_comment="PostComment",post=Post.objects.get(id=post_id),text=text)
				CreateCommentNotification(user,comment)
			elif type_of_post == "groupPost":
				comment = Comment.objects.create(user=user,type_of_comment="GroupPostComment",group_post=GroupPost.objects.get(id=post_id),text=text)
				comment.save()
			elif type_of_post == "shared":
				comment = Comment.objects.create(user=user,type_of_comment="SharedPostComment",share_post=SharePost.objects.get(id=post_id),text=text)
				comment.save()	
			elif type_of_post == "groupShared":
				comment = Comment.objects.create(user=user,type_of_comment="GroupSharedPostComment",group_shared_post=GroupSharePost.objects.get(id=post_id),text=text)
				comment.save()
			elif type_of_post == "feeling_post":
				comment = Comment.objects.create(user=user,type_of_comment="FeelingPostComment",feeling_post=Feelings.objects.get(id=post_id),text=text)
				comment.save()
			elif type_of_post == "sharedFeelingPost":
				comment = Comment.objects.create(user=user,type_of_comment="FeelingSharedPostComment",feeling_shared_post=ShareFeelingsPosts.objects.get(id=post_id),text=text)
				comment.save()
		
		elif "like" in request.POST:
			comment = Comment.objects.get(id=request.POST["comment"],type_of_comment=request.POST["type_of_comment"])
			if Account.objects.get(user=request.user) in comment.likes.all():
				comment.likes.remove(Account.objects.get(user=request.user))
			else:
				comment.likes.add(Account.objects.get(user=request.user))
		elif "reply_like" in request.POST:
			reply_comm = CommentReply.objects.get(id=request.POST["comment"])
			if Account.objects.get(user=request.user) in reply_comm.likes.all():
				reply_comm.likes.remove(Account.objects.get(user=request.user))
			else:
				reply_comm.likes.add(Account.objects.get(user=request.user))
		elif "post_text" in request.POST and request.FILES.get("img")==None:
			text = request.POST['post_text']
			if len(text)>0:
				new_post = Post.objects.create(user=user,caption=text,post_type="post")
				new_post.save()
				CreatePostNotification(user,new_post)
		elif "post_text" in request.POST and request.FILES.get('img')!=None:
			new_post = Post.objects.create(user=user,caption=request.POST["post_text"],post_type="post",file=request.FILES.get("img"))
			new_post.save()
			CreatePostNotification(user,new_post)
		elif "group_post_text" in request.POST:
			text = request.POST["group_post_text"]
			group = Group.objects.get(id=request.POST["group"])
			GroupPost.objects.create(user=user,group=group,post_type="groupPost",caption=text).save()
		elif "post_type" in request.POST:
			try:
				SavedPosts.objects.filter(user=user,post_type=request.POST["post_type"],post_id=request.POST["post_id"]).exists()
			except SavedPosts.DoesNotExist:
				SavedPosts.objects.create(user=user,post_type=request.POST["post_type"],post_id=request.POST["post_id"]).save()
		elif "post_like" in request.POST:
			emotion = list(request.POST)[1][:-2]
			if "post" in request.POST:
				post = Post.objects.get(id=request.POST['post_like']) 
			elif "shared_post" in request.POST:
				post = SharePost.objects.get(id=request.POST["post_like"])
			elif "group_original_post" in request.POST:
				post = GroupPost.objects.get(id=request.POST['post_like'])
			elif "group_shared_post" in request.POST:
				post = GroupSharePost.objects.get(id=request.POST['post_like'])
			elif "feeling_post" in request.POST:
				post = Feelings.objects.get(id=request.POST["post_like"])
			elif "sharedFeelingPost" in request.POST:
				post = ShareFeelingsPosts.objects.get(id=request.POST["post_like"])

			if user not in post.likes.all():
				self.filter_post_reactions(post,user)
				if emotion == 'like':
					post.like_reaction.add(user)				
				elif emotion == 'love':
					post.love_reaction.add(user)
				elif emotion == 'haha':
					post.haha_reaction.add(user)
				elif emotion == 'wow':
					post.wow_reaction.add(user)
				elif emotion == 'sad':
					post.sad_reaction.add(user)
				else:
					post.angry_reaction.add(user)
				post.likes.add(user)
				post.save()
			else:
				self.filter_post_reactions(post,user)
		elif "check" in request.POST:
			group_to_invite = Group.objects.get(id=request.POST["g"])
			for i in request.POST.getlist("check"):
				receiver=Account.objects.get(id=i)
				if not GroupInviteNotifications.objects.filter(sender=user,receiver=receiver,group_to_invite=group_to_invite).exists():
					GroupInviteNotifications.objects.create(sender=user,receiver=receiver,group_to_invite=group_to_invite,text=request.POST["textt"]).save()

		elif "add_friend" in request.POST:
			excepted_html_form_names = ["from_user","to_user","add_friend"]
			is_secure = self.check_html_forms_for_friend_request_system(request.POST,excepted_html_form_names,kwargs.get("pk"))
			if is_secure==False:
				return redirect(request.META["HTTP_REFERER"])
			self.make_friend_request(request.POST["from_user"],request.POST["to_user"])
		elif "rm-request" in request.POST:
			excepted_html_form_names = ["from_user","to_user","rm-request"]
			is_secure = self.check_html_forms_for_friend_request_system(request.POST,excepted_html_form_names,kwargs.get("pk"))
			if is_secure==False:
				return redirect(request.META["HTTP_REFERER"])
			self.remove_friend_request(request.POST["from_user"],request.POST["to_user"])
		elif "rm-friend" in request.POST:
			excepted_html_form_names = ["from_user","to_user","rm-friend"]
			is_secure = self.check_html_forms_for_friend_request_system(request.POST,excepted_html_form_names,kwargs.get("pk"))
			if is_secure==False:
				return redirect(request.META["HTTP_REFERER"])
			self.remove_friend(request.POST["from_user"],request.POST["to_user"])
		elif "join" in request.POST:
			g = Group.objects.get(id=request.POST["g"])
			g.members.add(user)
			g.save()
		elif "lvg" in request.POST:
			g = Group.objects.get(id=request.POST["g"])
			g.members.remove(user)
			g.save()

		elif "theme" in request.POST:
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()		
		return redirect(request.META["HTTP_REFERER"])

	def filter_post_reactions(self,post,user):
		post.likes.remove(user)
		post.like_reaction.remove(user)
		post.love_reaction.remove(user)
		post.haha_reaction.remove(user)
		post.wow_reaction.remove(user)
		post.sad_reaction.remove(user)
		post.angry_reaction.remove(user)
		post.save()
		return redirect(self.request.META["HTTP_REFERER"])

	def make_friend_request(self,from_user,to_user):
		f,t = self.get_from_to_users(from_user,to_user)	
		if not FriendRequest.objects.filter((Q(from_user=f) & Q(to_user=t)) | (Q(from_user=t) & Q(to_user=f))).exists():
			FriendRequest.objects.create(from_user=f,to_user=t).save()

	def remove_friend_request(self,from_user,to_user):
		f,t = self.get_from_to_users(from_user,to_user)
		try:
			FriendRequest.objects.get(from_user=f,to_user=t).delete()
		except FriendRequest.DoesNotExist:
			return redirect(self.request.META["HTTP_REFERER"])

	def get_from_to_users(self,f,t):
		from_user = Account.objects.get(id=f)
		to_user = Account.objects.get(id=t)
		return from_user,to_user

	def remove_friend(self,m,f):
		m,f = self.get_from_to_users(m,f)
		m.friends.remove(f.user)
		f.friends.remove(m.user)
		m.save()
		f.save()

	def check_html_forms_for_friend_request_system(self,reqs,excepted_data,displayed_user_id):
		if self.get_user_acc(reqs['from_user'])!=self.current_user() or self.get_user_acc(reqs['to_user'])!=self.get_user_acc(self.kwargs.get("pk")):
			return False
		return True

	def current_user(self):
		return Account.objects.get(user=self.request.user)

	def get_user_acc(self,i):
		try:
			return Account.objects.get(id=i)
		except Account.DoesNotExist:
			return None

class PageMixin(object):

	def get_context_data(self,*args,**kwargs):
		context = super(PageMixin,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=self.request.user)
		friends = [Account.objects.get(user=friend) for friend in context["my_profile"].friends.all()]
		context["accounts"]=friends
		friends.append(context["my_profile"])
		posts = []
		p=[]
		stories=[]
		for i in friends:
			if Post.objects.filter(user=i).exists():
				self.add_posts(Post.objects.filter(user=i),p)
			if SharePost.objects.filter(user=i).exists():
				self.add_posts(SharePost.objects.filter(user=i),p)
			if GroupPost.objects.filter(user=i).exists():
				self.add_posts(GroupPost.objects.filter(user=i),p,True)
			if Feelings.objects.filter(user=i).exists():
				self.add_posts(Feelings.objects.filter(user=i),p)
			if ShareFeelingsPosts.objects.filter(user=i).exists():
				self.add_posts(ShareFeelingsPosts.objects.filter(user=i),p)
			if GroupSharePost.objects.filter(user=i).exists():
				self.add_posts(GroupSharePost.objects.filter(user=i),p)
			if Story.objects.filter(user=i).exists():
				for j in Story.objects.filter(user=i):
					stories.append(j)
		posts.extend(p)
		posts.sort(key=attrgetter("created_at"))
		context["posts"] = reversed(posts)
		friends.pop(friends.index(context["my_profile"]))

		tag_list = []
		tag_list.extend(Account.objects.all()) 
		tag_list.extend(Group.objects.all())
		context["tag_list"] = tag_list;
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		visits = GroupVisitors.objects.filter(visitor=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		shortcuts = []
		for visit in visits:
			if visit.count >= 10:
				shortcuts.append(visit)
		context["shortcuts"]=shortcuts
		context["stories"]=stories
		return context

	def add_posts(self,posts,p,g=None):
		if g:
			for i in posts:
				if i.group.visibility != "hidden":
					p.append(i)
		else:
			for i in posts:
				p.append(i)

@method_decorator(login_required,name='dispatch')
class Search(ListView):
	model = Account
	template_name = "mainApp/search.html"

	def get_context_data(self,*args,**kwargs):
		context = super(Search,self).get_context_data(**kwargs)
		context["my_profile"]=Account.objects.get(user=self.request.user)
		return context

	def get(self,request,*args,**kwargs):
		query = self.request.GET.get('q')
		u = User.objects.filter(Q(username__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query))
		users = [Account.objects.get(user=i) for i in u]
		groups = Group.objects.filter(Q(group_name__icontains=query))
		len_of_users = len(users)
		len_of_groups = len(groups)
		my_profile = Account.objects.get(user=self.request.user)
		return render(self.request,"mainApp/search.html",{"users":users,
			"groups":groups,
			"my_profile":my_profile,
			"group_len":len_of_groups,
			"count_new_msgs":len(Message.objects.filter(to_user=Account.objects.get(user=self.request.user),seen=False)),
			"new_notifications":new_notification_counter(my_profile.id),
			"user_len":len_of_users})

@method_decorator(login_required,name='dispatch')
class Report(View):
	def get(self,request,*args,**kwargs):
		user = Account.objects.get(id=self.request.user.id)
		return render(request,"mainApp/report_center.html",ReportAndHelp("report",user))

	def post(self,request,*args,**kwargs):
		if "theme" in request.POST:
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()
		return redirect(request.META["HTTP_REFERER"])

@method_decorator(login_required,name='dispatch')
class Help(View):
	def get(self,request,*args,**kwargs):
		user = Account.objects.get(user=request.user)
		return render(request,"mainApp/report_center.html",{"my_profile":user,
			"count_new_msgs":len(Message.objects.filter(to_user=user,seen=False)),
			"new_notifications":new_notification_counter(user.id)})

@method_decorator(login_required,name='dispatch')
class FeelingsStatus(FormView):
	model = Feelings
	form_class = FeelingsForm
	template_name = "mainApp/feelings.html"
	context_object_name = "form"

	def form_valid(self,form):
		form.instance.user = self.user(self.request.user.id)
		form.save()
		return super(FeelingsStatus,self).form_valid(form)

	def get_context_data(self,*args,**kwargs):
		context = super(FeelingsStatus,self).get_context_data(**kwargs)
		context["my_profile"] = self.user(self.request.user.id)
		return context

	def user(self,id):
		return Account.objects.get(user=User.objects.get(id=id))

	def get_success_url(self):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class Home(PostMixins,PageMixin,ListView):	
	model = Post	
	template_name = 'mainApp/home.html'
