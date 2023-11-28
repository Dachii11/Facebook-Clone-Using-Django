from django.shortcuts import render,redirect
from accounts.models import Account,GroupSharePost,GroupPost,Group,GroupVisitors
from accounts.views import ThemeMixin
from posts.models import Post,SharePost,SavedPosts
from notifications.views import CreatePostNotification,new_notification_counter
from django.contrib import messages
from chat.models import Message
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView,CreateView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from mainApp.views import PostMixins
from django.urls import reverse_lazy
from comments.models import Comment
from mainApp.models import ShareFeelingsPosts,Feelings
from pathlib import Path
from operator import attrgetter
import os

class PostPageMixin(object):
	def get(self,request,*args,**kwargs):
		try:
			self.object = self.model.objects.get(id=kwargs.get("pk"))
		except self.model.DoesNotExist:
			return redirect(request.META['HTTP_REFERER'])
		self.me = Account.objects.get(user=User.objects.get(username=self.request.user))
		try:
			if self.me not in self.object.views.all():
				self.object.views.add(self.me)
			self.object.save()
		except AttributeError:
			None
		post = self.get_context_data(object=self.get_object)
		return render(request,"posts/post_detail.html",post)

class PostDeleteMixin(object):
	success_url = reverse_lazy("mainApp:index")
	template_name = "posts/post_confirm_delete.html"

class PostFileRemoveMixin(object):
	def get_success_url(self):
		if len(self.request.get_full_path().split("/"))==5:
			self.post = Post.objects.get(id=self.request.get_full_path().split("/")[3])
		else:
			self.post = GroupPost.objects.get(id=self.request.get_full_path().split("/")[4])
		try:
			self.file = str(self.post.file.url).replace('/','\\').split('\\')[-1]
			self.parent_folders = "\\".join(str(Path(str(self.post.file.url)).parent.absolute()).split("\\")[1:])
			self.remove_img_from_os(self.parent_folders,self.file)
		except ValueError:
			pass
		return reverse_lazy("mainApp:index")

	def remove_img_from_os(self,folders,file):
		path = "\\".join(str(Path(str(file)).parent.absolute()).split('\\'))+f"\\{folders}\\{file}"
		os.remove(path)

@method_decorator(login_required,name='dispatch')
class SharedPostDetail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = SharePost

	def get_context_data(self,*args,**kwargs):
		context = super(SharedPostDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = SharePost.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(share_post=context["post"],type_of_comment="SharedPostComment")
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class GroupPostDetail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = GroupPost

	def get_context_data(self,*args,**kwargs):
		context = super(GroupPostDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = GroupPost.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(group_post=context["post"],type_of_comment="GroupPostComment")
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["allow_all_comments"] = True
		return context

@method_decorator(login_required,name='dispatch')
class Group_shared_post_detail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = GroupSharePost
	template_name = "posts/post_detail.html"

	def get_context_data(self,*args,**kwargs):
		context = super(Group_shared_post_detail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = GroupSharePost.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(group_shared_post=context["post"],type_of_comment="GroupSharedPostComment")
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["allow_all_comments"] = True
		print(context["post"].post_type)
		return context

# @method_decorator(login_required,name='dispatch')
class AccountMixin(object): 
	def get_context_data(self,*args,**kwargs):
		context = super(AccountMixin,self).get_context_data(**kwargs)
		context['my_profile'] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["shortcuts"] = visits_count(context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["allow_all_comments"] = True
		return context

@method_decorator(login_required,name='dispatch')
class PostDetail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = Post

	def get_context_data(self,*args,**kwargs):
		context = super(PostDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = Post.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(post=context["post"],type_of_comment="PostComment")
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["allow_all_comments"] = True
		return context

@method_decorator(login_required,name='dispatch')
class FeelingPostDetail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = Feelings

	def get_context_data(self,*args,**kwargs):
		context = super(FeelingPostDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = Feelings.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(feeling_post=context["post"],type_of_comment="FeelingPostComment")
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["allow_all_comments"] = True
		return context

@method_decorator(login_required,name='dispatch')
class FeelingPostSharedDetail(PostPageMixin,PostMixins,SingleObjectMixin,View):
	model = ShareFeelingsPosts

	def get_context_data(self,*args,**kwargs):
		context = super(FeelingPostSharedDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["post"] = ShareFeelingsPosts.objects.get(id=self.request.get_full_path().split("/")[3])
		context["comments"] = Comment.objects.filter(feeling_shared_post=context["post"],type_of_comment="FeelingSharedPostComment")
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["allow_all_comments"] = True
		return context

@method_decorator(login_required,name='dispatch')
class DeletePost(PostFileRemoveMixin,DeleteView):
	model = Post
	template_name = "posts/post_confirm_delete.html"

	def get_context_data(self,*args,**kwargs):
		context = super(DeleteView,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class DeleteSharedPost(PostDeleteMixin,AccountMixin,DeleteView):
	model = SharePost

@method_decorator(login_required,name='dispatch')
class DeleteGroupSharedPost(PostDeleteMixin,AccountMixin,DeleteView):
	model = GroupSharePost

@method_decorator(login_required,name='dispatch')
class DeleteGroupPost(PostDeleteMixin,PostFileRemoveMixin,AccountMixin,DeleteView):
	model = GroupPost

@method_decorator(login_required,name='dispatch')
class DeleteFeelingPost(PostDeleteMixin,AccountMixin,DeleteView):
	model = Feelings

@method_decorator(login_required,name='dispatch')
class DeleteSharedFeelingPost(PostDeleteMixin,AccountMixin,DeleteView):
	model = ShareFeelingsPosts
	
@method_decorator(login_required,name='dispatch')
class Share_Post(AccountMixin,CreateView):
	model = SharePost
	fields = ("caption","status","tags")
	template_name = "posts/share_post.html"

	def get(self,request,*args,**kwargs):
		try:
			self.object = Post.objects.get(id=kwargs.get("pk"))
			post = self.get_context_data(object=self.get_object)
			return render(request,self.template_name,post)
		except Post.DoesNotExist:
			return redirect(request.META["HTTP_REFERER"])

	def form_valid(self,form):
		user = Account.objects.get(user=User.objects.get(username=self.request.user))
		form.instance.user = user
		form.instance.post_type = "shared"
		
		referer_post = Post.objects.get(id=self.request.get_full_path().split("/")[3])
		form.instance.referer_post = referer_post
		form.save()
		return super(Share_Post,self).form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class FeelingPostShare(AccountMixin,CreateView):
	model = ShareFeelingsPosts
	fields = ("caption",)
	template_name = "posts/share_post.html"

	def form_valid(self,form):
		form.instance.user = Account.objects.get(user=User.objects.get(username=self.request.user))
		form.instance.post_type = "sharedFeelingPost"
		form.instance.referer_post = Feelings.objects.get(id=self.request.get_full_path().split("/")[3])
		form.save()
		return super(FeelingPostShare,self).form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class ShareGroupPost(AccountMixin,CreateView):
	model = GroupSharePost
	fields = ("caption",)
	template_name = "posts/share_post.html"

	def form_valid(self,form):
		form.instance.user = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		form.instance.post_type = "groupShared"
		form.instance.referer_post = GroupPost.objects.get(id=self.request.get_full_path().split("/")[3])
		form.save()
		return super(ShareGroupPost,self).form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class AddPost(AccountMixin,CreateView):
	model = Post
	fields = ("file","caption","location","status","tags","feeling")
	template_name = "posts/add_post.html"
	def form_valid(self,form):
		form.instance.user = self.creator()
		form.instance.post_type = "post"
		if form.cleaned_data["file"]:
			if form.cleaned_data["file"].size> 20971520:
				messages.error(self.request,"File is too large. Maximum 20MB")
				return redirect(self.request.META["HTTP_REFERER"])
		form.save()
		return super(AddPost,self).form_valid(form)

	def get_success_url(self, **kwargs):
		CreatePostNotification(self.creator(),self.object)
		return reverse_lazy("mainApp:index")

	def creator(self):
		return Account.objects.get(user=self.request.user)

@method_decorator(login_required,name='dispatch')
class Watch(AccountMixin,PostMixins,ListView):
	model = GroupPost
	template_name = "posts/watch.html"
	context_object_name = "videos"
	def get_queryset(self):
		videos = []
		videos.extend(list([post for post in GroupPost.objects.all() if post.media_type_html()=="video"]))
		return videos

@method_decorator(login_required,name='dispatch')
class Saves(AccountMixin,PostMixins,ListView):
	model = SavedPosts
	template_name = "posts/saved_posts.html"
	context_object_name = "posts"

	def get_queryset(self):
		posts = []
		all_saved_post = SavedPosts.objects.filter(user=Account.objects.get(user=self.request.user))
		for post in all_saved_post:
			if post.post_type == "post":
			    posts.append(Post.objects.get(id=post.id))
			elif post.post_type == "shared":
				posts.append(SharePost.objects.get(id=post.id))
			elif post.post_type == "groupPost":
			    posts.append(GroupPost.objects.get(id=post.id))
			elif post.post_type == "groupShared":
				posts.append(GroupSharePost.objects.get(id=post.id))
			posts.sort(key=attrgetter("created_at"))
			return posts

def visits_count(visitor):
	visits = GroupVisitors.objects.filter(visitor=visitor)
	shortcuts = []
	for visit in visits:
		if visit.count >= 10:
			shortcuts.append(visit)
	return shortcuts

