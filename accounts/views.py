from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView,SingleObjectMixin
from django.views.generic.edit import DeleteView,FormView,UpdateView,CreateView
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .token import account_activation_token
from .models import Account,Group,GroupPost,GroupSharePost,FriendRequest,GroupVisitors,GroupRules,Report
from chat.models import Message
from mainApp.views import PageMixin,Home,PostMixins
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserRegisterForm,GroupCreateForm,GroupPostForm,RuleAddForm,GroupEditForm,GroupReportForm,EditProfile,LoginForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from mainApp.models import Feelings,ShareFeelingsPosts,Logs
from notifications.models import GroupInviteNotifications
from posts.models import Post,SharePost
from operator import attrgetter
import requests
import os
from django.contrib import messages
from django.db.models import Q,F
from notifications.views import new_notification_counter
from django.contrib.auth.mixins import LoginRequiredMixin
from comments.models import Comment
from pathlib import Path
from django.contrib.auth.decorators import user_passes_test
from django.template.defaulttags import register


class RemoveFile:
	def __init__(self,file):
		self.file = file

	def remove_file(self):
		try:
			f = str(self.file).replace('/','\\').split('\\')[-1]
			parent_folders = "\\".join(str(Path(str(self.file)).parent.absolute()).split("\\")[1:])
			print(parent_folders)
			if parent_folders!="media":
				path = "\\".join(str(Path(str(f)).parent.absolute()).split("\\"))+f"\\{parent_folders}\\{f}"
				os.remove(path)
		except FileNotFoundError:
			return
			
class ThemeMixin(object):
	def post(self,request,*args,**kwargs):
		user = Account.objects.get(user=request.user)
		if "theme" in request.POST:
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()	
			return redirect(request.META["HTTP_REFERER"])

class PagePermissionMixin(object):
	def get_context_data(self,*args,**kwargs):
		context = super(PagePermissionMixin,self).get_context_data(**kwargs)
		user = Account.objects.get(user=self.request.user)
		group = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		if user not in group.admin.all():
			return HttpResponse("Permission denied!")
		return context

class ProfileMixin(object):
	def get_context_data(self,*args,**kwargs):
		context = super(ProfileMixin,self).get_context_data(**kwargs)
		posts = []
		user = Account.objects.get(id=self.request.get_full_path().split("/")[3])
		me = Account.objects.get(user=User.objects.get(id=self.request.user.id))
	
		account_visibility = user.who_can_see_my_posts
		if  (user==me) or account_visibility=="Public" or (account_visibility=="Friends" and me.user in user.friends.all()) or (account_visibility=="Only me" and user==me):
			post_data=Post.objects.filter(user=user)
			posts.extend(list(post_data))
			posts.extend(list(SharePost.objects.filter(user=user)))
			posts.extend(list(GroupSharePost.objects.filter(user=user)))
			posts.extend(list(Feelings.objects.filter(user=user)))
			posts.extend(list(ShareFeelingsPosts.objects.filter(user=user)))
			posts.sort(key=attrgetter("created_at"))
			context["posts"] = reversed(posts)
			context["images"] = [image_post for i,image_post in enumerate(post_data,start=1) if (image_post.file != "" and image_post.media_type_html()=="image") and i<=2]
			more_images=[i for i in post_data if i.file!=""]
			if len(more_images)>6:
				context["more_images_count"]=len(more_images)-2
			try:
				obj = FriendRequest.objects.get(from_user=me,to_user=user)
				me_in_requests = True
			except FriendRequest.DoesNotExist:
				me_in_requests = False
			context["me_in_requests"] = me_in_requests
			context["permission"]=True
		else:
			context["permission"]=False
		who_can_send_me_friend_request = user.who_can_send_me_friend_request
		if (user==me) or who_can_send_me_friend_request=="Everyone" or (who_can_send_me_friend_request=="Friends of Friends" and user.user in [friend.friends.all() for friend in user.friends.all()]):
			context["friend_request_permission"] = True
		else:
			context["friend_request_permission"] = False
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["account"] = user 
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		who_can_see_my_friends = user.who_can_see_my_friends_list
		if (user==me) or who_can_see_my_friends=="Everyone" or (who_can_see_my_friends=="Friends" and user.user in me.friends.all()) or (who_can_see_my_friends=="Only Me" and user==me):
			context["friends"] = [Account.objects.get(user=user) for user in user.friends.all()]
		else:
			context["friends"] = None

		if (user==me) or user.who_can_see_my_email_address=="Everyone" or (user.who_can_see_my_email_address=="Friends" and user.user in me.friends.all()):
			context["email_view_permission"] = True

		context["mfl"] = len(user.friends.filter(pk__in=context["my_profile"].friends.all()))

		return context
        
class ProfileAccountMixin(object):
	def get_context_data(self,*args,**kwargs):
		context = super(ProfileAccountMixin,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=self.request.user)
		context["shortcuts"] = visits_count(context["my_profile"])
		context["my_groups"] = Group.objects.filter(admin=context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class Profile(PostMixins,ProfileMixin,SingleObjectMixin,View):
	model = Account
	def get(self,request,*args,**kwargs):
		self.object = self.get_object()
		account = self.get_context_data(object=self.object)
		my_profile = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		only_friends = account in my_profile.friends.all()
		return render(request,"accounts/account_detail.html",account)

@method_decorator(login_required,name='dispatch')
class GroupDetail(PostMixins,SingleObjectMixin,View):
	model = Group

	def get(self,request,*args,**kwargs):
		self.object = self.get_object()
		group = self.get_context_data(object=self.object)
		visitor =Account.objects.get(user=User.objects.get(username=self.request.user))
		g = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		try:
			visit = GroupVisitors.objects.get(group=g,visitor=visitor)
			visit.count = F('count')+1
			visit.save()
		except GroupVisitors.DoesNotExist:
			new_visit = GroupVisitors.objects.create(group=g,visitor=visitor)
			new_visit.count = F('count')+1
			new_visit.save()
		return render(request,"accounts/group_detail.html",group)

	def get_context_data(self,*args,**kwargs):
		context = super(GroupDetail,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		group = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		context["members"] = group.members.all()
		context["friends"] = [Account.objects.get(user=acc) for acc in list(context["my_profile"].friends.all()) if acc not in group.members.all()]
		context["posts"] = GroupPost.objects.filter(group=group)
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		not_member_private_group = group.privacy == "Private" and context["my_profile"] not in group.members.all()
		context["me_in_group"] = False
		if context["my_profile"] in group.members.all():
			context["me_in_group"] = True
		if not_member_private_group:
			context["can_post"] = False
		elif not not_member_private_group:
			if group.who_can_post == 'Everyone' or (group.who_can_post=='Only Admins' and context["my_profile"] in group.admin.all()):
				context["can_post"] = True
			else:
				context["can_post"] = False
		return context

class SignIn(View):
	template_name = "accounts/login.html"

	def get(self,request,*args,**kwargs):
		print(request)
		return render(request,self.template_name,{"form":LoginForm})

	def post(self,request,*args,**kwargs):
		form = LoginForm(request.POST)
		print(f"{request.POST['username']}\n{request.POST['password']}")
		user = authenticate(username=request.POST['username'],password=request.POST['password'])
		if user is not None:
			acc = Account.objects.get(user=user)
			try:
				data = get_location(request)
				log=Logs.objects.create(account_logged_in=acc,ip_address=data["ip"],user_agent=data["user_agent"],city=data["city"],country=data["country"])
				log.save()
				if log.ip_address!=Logs.objects.filter(account_logged_in_id=user.id).first().ip_address:
					current_site = get_current_site(self.request)
					mail_subject = "New Loggin to your account."
					message = render_to_string("accounts/confirm_account.html",{
							"user":user,
							"domain":current_site.domain,
							"uid":urlsafe_base64_encode(force_bytes(user.pk)),
							"token":account_activation_token.make_token(user),
						})
					TO_EMAIL = user.email
					email = EmailMessage(mail_subject,message,to=[TO_EMAIL])
					email.send()
			except TypeError:
				print("Site is probably on localhost and can't get data from User IP.")
			finally:
				login(request,user)
				return redirect("mainApp:index")
		else:
			messages.error(request,"Invalid Credentials!")
			return redirect(request.META["HTTP_REFERER"])

class SignUp(CreateView):
	template_name = 'accounts/signup.html'
	form_class = UserRegisterForm

	def get_context_data(self,*args,**kwargs):
		context = super(SignUp,self).get_context_data(**kwargs)
		countries = []
		with open("mainApp/countries.txt","r") as f:
			for i in f.readlines():
				countries.append(i.replace("\n",''))
		context["countries"]=countries
		return context

	def form_valid(self,form):
		username = form.cleaned_data['username']
		password = form.cleaned_data["password1"]
		email = form.cleaned_data["email"]
		country = self.request.POST["country"]
		gender = self.request.POST["gender"]
		if User.objects.filter(email=email).exists():
			messages.warning(self.request,"This Email Already exists!")
			return redirect(self.request.META["HTTP_REFERER"])
		else:
			form = UserRegisterForm(self.request.POST)
			if form.is_valid():
				user = form.save(commit=False)	# save form in the memory not in database
				user.is_active = False
				user.save()
				new_user = User.objects.get(username=username)
				acc=Account.objects.create(user=new_user,from_country=country,username=username,gender=gender,id_user=new_user.id)
				acc.save()
				current_site = get_current_site(self.request)
				mail_subject = "Activation link has been sent to your email"
				message = render_to_string("accounts/acc_active_email.html",{
						"user":user,
						"domain":current_site.domain,
						"uid":urlsafe_base64_encode(force_bytes(user.pk)),
						"token":account_activation_token.make_token(user),
					})
				TO_EMAIL = self.request.POST["email"]
				email = EmailMessage(mail_subject,message,to=[TO_EMAIL])
				email.send()

				return HttpResponse("Please confirm your email address to complete the registration")

	def get_success_url(self,**kwargs):
		return reverse_lazy("mainApp:index")

def activate(request,uidb64,token):
	user = request.user
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user,token):
		user.is_active = True
		user.save()
		return HttpResponse("Thank you for your email confirmation. Now you can login your account.")
	else:
		return HttpResponse("Activation link is invalid!")

@method_decorator(login_required,name='dispatch')
class Groups(ProfileAccountMixin,ListView):
	model = Group
	template_name = "accounts/groups.html"
	context_object_name = "groups"

	def post(self, request, *args, **kwargs):
		self.object_list = self.get_queryset()
		if "theme" in request.POST:
			user = Account.objects.get(user=request.user)
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()	
			return redirect(request.META["HTTP_REFERER"])
		elif "searchGroup" in request.POST:
			search = request.POST["searchGroup"].strip()
			self.groups = Group.objects.filter(Q(group_name__contains=search) | Q(description__contains=search) | Q(group_type__contains=search))
			self.group_type = "All"
		elif "general" in request.POST:
			self.groups = Group.objects.filter(group_type="General")
			self.group_type = "General"
		elif "BuyAndSell" in request.POST:
			self.groups = Group.objects.filter(group_type="Buy and Sell")
			self.group_type = "Buy and Sell"
		elif "gaming" in request.POST:
			self.groups = Group.objects.filter(group_type="Gaming")
			self.group_type = "Gaming"
		elif "job" in request.POST:
			self.groups = Group.objects.filter(group_type="Job")
			self.group_type = "Job"
		elif "parenting" in request.POST:
			self.groups = Group.objects.filter(group_type="Parenting")
			self.group_type = "Parenting"
		else:
			self.groups = Group.objects.all()
			self.group_type = "All"
			
		self.found_groups_count = len([group for group in self.groups.all() if group.visibility != "Hidden"])
		self.account = Account.objects.get(user=User.objects.get(username=request.user))
		self.filter_groups = []
		for group in self.groups.all():
			if group.visibility == "Visible":
				self.filter_groups.append(group)
		return render(request,"accounts/groups.html",{"groups":self.filter_groups,"my_profile":self.account,
					"found":self.found_groups_count,"type":self.group_type,
					"count_new_msgs":len(Message.objects.filter(to_user=self.account,seen=False)),
					"new_notifications":new_notification_counter(self.account.id)})
		
	def get_context_data(self,*args,**kwargs):
		context = super(Groups,self).get_context_data(**kwargs)
		self.filter_groups = []
		groups = Group.objects.all()
		for group in groups.all():
			if group.visibility == "Visible" or Account.objects.get(user=User.objects.get(id=self.request.user.id)) in group.admin.all():
				self.filter_groups.append(group)

		context['groups'] = self.filter_groups
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class CreateGroup(ProfileAccountMixin,FormView):
	form_class = GroupCreateForm
	template_name = "accounts/create_group.html"
	context_object_name = "form"

	def form_valid(self,form):
		form.save()
		form.instance.admin.add(Account.objects.get(user=self.request.user))
		form.instance.members.add(Account.objects.get(user=self.request.user))
		return super(CreateGroup,self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class Suggestions(ListView):
	model = Account
	template_name = "accounts/suggestions.html"
	context_object_name = "suggestions"

	def get_context_data(self,*args,**kwargs):
		context = super(Suggestions,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		context["requests"] = FriendRequest.objects.filter(to_user=context["my_profile"])
		context["shortcuts"] = visits_count(context["my_profile"])
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		context["suggestions"] = [acc for acc in Account.objects.all() if User.objects.get(username=acc.user) not in context["my_profile"].friends.all() and acc != context['my_profile']]
		self.mutual_friends = {}
		for i in context["suggestions"]:
			total_friends = i.friends.filter(pk__in=context["my_profile"].friends.all())
			self.mutual_friends.update({f"{i}":len(total_friends)})
		context["mutuals"] = self.mutual_friends
		return context

	def post(self,request,*args,**kwargs):
		user = Account.objects.get(user=request.user)
		if "theme" in request.POST:
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()
		return redirect(request.META["HTTP_REFERER"])

class FriendRequests(ProfileAccountMixin,ListView):
	model = FriendRequest
	template_name = "accounts/friend_suggs.html"
	context_object_name = "requests"

	def post(self,request,*args,**kwargs):
		from_user = Account.objects.get(user=User.objects.get(username=request.POST["from_user"]))
		to_user = Account.objects.get(user=request.user)
		try:
			FriendRequest.objects.filter(from_user=from_user,to_user=to_user).exists()
			if "accept" in request.POST:
				from_user.friends.add(User.objects.get(username=request.user))
				to_user.friends.add(User.objects.get(username=request.POST["from_user"]))
			FriendRequest.objects.get(from_user=from_user,to_user=to_user).delete()
		except FriendRequest.DoesNotExist:
			return redirect(request.META['HTTP_REFERER'])
		return redirect(request.META['HTTP_REFERER'])

@method_decorator(login_required,name='dispatch')
class CreateGroupPost(ProfileAccountMixin,FormView):
	model = GroupPost
	form_class = GroupPostForm
	template_name = "accounts/create_group_post.html"

	def get(self,*args,**kwargs):
		group = Group.objects.get(id=self.request.get_full_path().split("/")[3])
		mp = Account.objects.get(user=self.request.user)
		if mp not in group.admin.all():
			return HttpResponse("Permission denied!")
		return render(self.request,self.template_name,{"form":self.form_class,"my_profile":mp})

	def form_valid(self,form):
		form.instance.post_type = "groupPost"
		form.instance.user = Account.objects.get(user=User.objects.get(username=self.request.user))
		form.instance.group = Group.objects.get(id=self.request.get_full_path().split('/')[3]) 
		form.save()
		return super(CreateGroupPost,self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class Friends(ProfileAccountMixin,ListView):
	model = Account
	template_name = "accounts/suggestions.html"
	context_object_name = "suggestions"

	def get_queryset(self):
		me = Account.objects.get(user=self.request.user)
		return [Account.objects.get(user=account) for account in me.friends.all()]

@method_decorator(login_required,name='dispatch')
class GroupAbout(ThemeMixin,SingleObjectMixin,View):
	model = Group
	template_name = "accounts/group_about.html"
	context_object_name = "group"

	def get(self,request,*args,**kwargs):
		g = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		my_profile = Account.objects.get(user=request.user)
		data = {"group":g,"my_profile":my_profile,"count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False))}
		if g.who_can_post == 'Everyone' or (g.who_can_post=='Only Admins' and my_profile in g.admin.all()):
			data.update({"can_post":True})
		return render(request,"accounts/group_about.html",data)

class GroupMembers(ThemeMixin,SingleObjectMixin,View):
	model = Group
	def get(self,request,*args,**kwargs):
		g = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		my_profile = Account.objects.get(user=User.objects.get(username=self.request.user))
		members = g.members.all()
		my_profile = Account.objects.get(user=request.user)
		data = {"group":g,"my_profile":my_profile,"members":members,"count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False))}
		if g.who_can_post == 'Everyone' or (g.who_can_post=='Only Admins' and my_profile in g.admin.all()):
			data.update({"can_post":True})
		return render(request,"accounts/group_members.html",data)

@method_decorator(login_required,name='dispatch')
class GroupRule(SingleObjectMixin,View):
	model = Group
	template_name = "accounts/group_rules.html"

	def get(self,request,*args,**kwargs):
		group = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		rules = GroupRules.objects.filter(group=group)
		my_profile = Account.objects.get(user=User.objects.get(username=self.request.user))
		return render(request,"accounts/group_rules.html",{"rules":rules,"group":group,"my_profile":my_profile,
				"count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False)),
				"new_notifications":new_notification_counter(my_profile.id)})

	def post(self,request,*args,**kwargs):
		if "remove_rule" in request.POST:
			GroupRules.objects.get(id=request.POST["remove_rule"]).delete()
		if "theme" in request.POST:
			user = Account.objects.get(user=request.user)
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
		return redirect(request.META["HTTP_REFERER"])

@method_decorator(login_required,name='dispatch')
class AddGroupRule(ThemeMixin,ProfileAccountMixin,FormView):
	model = GroupRules
	form_class = RuleAddForm
	template_name = "accounts/rule_add.html"

	def get(self,request,*args,**kwargs):
		user = Account.objects.get(user=self.request.user)
		if permission(user,Group.objects.get(id=self.request.get_full_path().split('/')[3])):
			return HttpResponse("Permission denied!")
		else:
			return render(request,"accounts/rule_add.html",{"my_profile":user,
				"count_new_msgs":len(Message.objects.filter(to_user=user,seen=False)),
				"form":RuleAddForm,
				"new_notifications":new_notification_counter(user.id)})	

	def post(self,request,*args,**kwargs):
		group = Group.objects.get(id=self.request.get_full_path().split('/')[3])
		GroupRules.objects.create(group=group,rule_body=request.POST["rule_body"],rule_title=request.POST["rule_title"]).save()
		return redirect("accounts:group",pk=str(Group.objects.get(id=kwargs.get("pk")).id))

@method_decorator(login_required,name='dispatch')
class EditGroup(ProfileAccountMixin,FormView):
	model = Group
	form_class = GroupEditForm
	context_object_name = "group"
	template_name = "accounts/groupedit.html"

	def get(self,request,*args,**kwargs):
		user = Account.objects.get(user=self.request.user)
		group=Group.objects.get(id=self.request.get_full_path().split('/')[3])
		web_address = f"{request.META['HTTP_HOST']}{'/'.join(request.get_full_path().split('/')[:-2])}/"
		if permission(user,group):
			return HttpResponse("Permission denied!")
		else:
			return render(request,"accounts/groupedit.html",{"my_profile":user,
							"count_new_msgs":len(Message.objects.filter(to_user=user,seen=False)),
							"new_notifications":new_notification_counter(user.id),
							"form":GroupEditForm(instance=group),
							"group":group,
							"web_address":web_address})	

	def post(self,request,*args,**kwargs):
		user = Account.objects.get(user=self.request.user) 
		if "theme" in request.POST:
			if user.theme==True:
				user.theme=False
			else:
				user.theme=True
			user.save()
		else:
			DEFAULT = "default_cover.png"
			group = Group.objects.get(id=kwargs.get("pk"))
			if "rci" in request.POST:
				group.group_cover.delete()
				group.group_cover = DEFAULT
				group.save()
			else:
				group_icon = group.group_cover.url
				remove = RemoveFile(group_icon)
				remove.remove_file()
				form = GroupEditForm(request.POST,request.FILES or None,instance=Group.objects.get(id=kwargs.get("pk")))
				form.save()
		return redirect(request.META["HTTP_REFERER"])

class DeleteGroup(ProfileAccountMixin,DeleteView):
	model = Group
	template_name = "accounts/group_delete.html"

	def get(self,request,*args,**kwargs):
		group = Group.objects.get(id=kwargs.get("pk"))
		pr = Account.objects.get(user=request.user)
		if pr not in group.admin.all():
			return HttpResponse("Permission denied")
		return render(request,self.template_name,{"my_profile":pr})

	def form_valid(self,form):
		return super(DeleteGroup,self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy("mainApp:index")

@method_decorator(login_required,name='dispatch')
class ReportGroup(FormView):
	model = Report
	template_name = "accounts/report.html"
	form_class = GroupReportForm

	def get_context_data(self,*args,**kwargs):
		context = super(ReportGroup,self).get_context_data(**kwargs)
		context['my_profile'] = Account.objects.get(user=self.request.user)
		context["group"] = self.get_group()
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

	def post(self,request,*args,**kwargs):
		form = GroupEditForm(request.POST)
		if form.is_valid():
			reported_group = self.get_group()
			who_reported = self.who_reported()
			why = request.POST["why"]
			problem = request.POST["problem"]
			text = request.POST["text"]
			Report.objects.create(report_group=reported_group,who_reported=who_reported,why=why,problem=problem,text=text).save()
		return redirect("accounts:group",pk=reported_group.id)

	def get_group(self):
		return Group.objects.get(id=self.request.get_full_path().split('/')[3])

	def who_reported(self):
		return Account.objects.get(user=self.request.user)

class ViewMixin(object):
	def get(self,request,*args,**kwargs):
		my_profile = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		context={"my_profile":my_profile,
				 "count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False)),
				 "new_notifications":new_notification_counter(my_profile.id)}
		return render(request,self.template_name,context)

class SettingsMixin(object):
	template_name = "accounts/who_can_see_my_friends_list.html"
	model = Account

	def get_object(self):
		return Account.objects.get(user=User.objects.get(id=self.request.user.id))
	def get_context_data(self,*args,**kwargs):
		context=super(SettingsMixin,self).get_context_data(**kwargs)
		context["my_profile"]=Account.objects.get(user=self.request.user)
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class Settings(ViewMixin,View):
	template_name = "accounts/settings.html"

@method_decorator(login_required,name='dispatch')
class WhoCanSeeMyPosts(SettingsMixin,UpdateView):
	fields = ("who_can_see_my_posts",)

	def get_success_url(self):
		return reverse_lazy("accounts:who_can_see_my_posts")

@method_decorator(login_required,name='dispatch')
class WhoCanSeeMyFriendList(SettingsMixin,UpdateView):
	fields = ("who_can_see_my_friends_list",)

	def get_success_url(self):
		return reverse_lazy("accounts:who_can_see_my_friends_list")

@method_decorator(login_required,name='dispatch')
class WhoCanSendMeFriendRequest(SettingsMixin,UpdateView):
	fields = ("who_can_send_me_friend_request",)

	def get_success_url(self):
		return reverse_lazy("accounts:who_can_send_me_friend_request")

@method_decorator(login_required,name="dispatch")
class WhoCanSeeMyEmailAddress(SettingsMixin,UpdateView):
	fields = ("who_can_see_my_email_address",)

	def get_success_url(self):
		return reverse_lazy("accounts:who_can_see_my_email_address")

@method_decorator(login_required,name='dispatch')
class EditProfile(SettingsMixin,UpdateView):
	template_name = "accounts/edit.html"
	form_class = EditProfile
	context_object_name = "form"

	def get_success_url(self):
		return self.request.META["HTTP_REFERER"]

def visits_count(visitor):
	visits = GroupVisitors.objects.filter(visitor=visitor)
	shortcuts = []
	for visit in visits:
		if visit.count >= 10:
			shortcuts.append(visit)
	return shortcuts

def permission(user,group):
	if user not in group.admin.all():
		return True

def get_location(reqs):
	ip_address,user_agent = get_ip(reqs)
	try:
		response = requests.get(f"https://ipapi.co/{ip_address}/json/").json()
		location_data = {
			"ip":ip_address,
			"user_agent":user_agent,
			"city":response.get("city"),
			"country":response.get("country_name"),
		}
	except requests.exceptions.ConnectionError:
		return
	return location_data

def get_ip(reqs):
	agent = reqs.META["HTTP_USER_AGENT"]
	x_forwarded_for = reqs.META.get("HTTP_X_FORWARDED_FOR")
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = reqs.META.get('REMOTE_ADDR')
	return ip,agent