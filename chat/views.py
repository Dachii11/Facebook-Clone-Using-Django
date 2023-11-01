from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.models import Account
from django.urls import reverse_lazy
from accounts.views import ProfileAccountMixin,ThemeMixin,ViewMixin,SettingsMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView,SingleObjectMixin
from django.views.generic.edit import CreateView,UpdateView,FormView,DeleteView
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.db.models import Q
from operator import attrgetter
from .models import Message,PrivateChat,ChatRoomGroup,GroupMessage
from .forms import AddGroupMemberForm
from notifications.views import new_notification_counter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

def get_msgs_nots(to_user):
		return len(Message.objects.filter(to_user=to_user,seen=False))

@method_decorator(login_required,name='dispatch')
class ChatHome(ThemeMixin,ListView):
	model = Account
	template_name = "chat/messanger.html"
	context_object_name = "friends"

	def get_context_data(self,*args,**kwargs):
		context = super(ChatHome,self).get_context_data(**kwargs)
		context["my_profile"] = Account.objects.get(user=User.objects.get(username=self.request.user))
		chat_with = PrivateChat.objects.filter(Q(user_1=context["my_profile"])|Q(user_2=context["my_profile"]))
		groups = ChatRoomGroup.objects.filter(members=context["my_profile"])
		not_seen_chat=[]
		seen_chat=[]
		for i in chat_with:
			if i.user_1==context["my_profile"] and i.user_1_seen==False or i.user_2==context["my_profile"] and i.user_2_seen==False:
				not_seen_chat.append(i)
			else:
				seen_chat.append(i)
		chat = []
		f=not_seen_chat+seen_chat
		chat.extend(list(groups))
		chat.extend(list(f))
		context["chat_with"]=chat
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class Redirect(DetailView):
	model = Account
	template_name = "chat/messanger.html"

	def get(self,request,*args,**kwargs):
		chat_with = Account.objects.get(id=request.get_full_path().split("/")[3])
		me = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		if PrivateChat.objects.filter(user_1=chat_with,user_2=me).exists():
			room = PrivateChat.objects.get(user_1=chat_with,user_2=me)
		elif PrivateChat.objects.filter(user_1=me,user_2=chat_with).exists():
			room = PrivateChat.objects.get(user_1=me,user_2=chat_with)
		else:
			room=PrivateChat.objects.create(user_1=me,user_2=chat_with)
		return redirect("chat:chat",pk=room.id)

@method_decorator(login_required,name='dispatch')
class Chat(ThemeMixin,DetailView):
	model = PrivateChat
	template_name = "chat/chat.html"

	def get_context_data(self,*args,**kwargs):
		context = super(Chat,self).get_context_data(**kwargs)
		chat = PrivateChat.objects.get(id=self.request.get_full_path().split("/")[2])

		my_profile = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		if chat.user_1==my_profile and chat.user_2==my_profile:
			chat.user_1_seen=True
			chat.user_2_seen=True
		
		if chat.user_1 == my_profile:
			friend = chat.user_2
			chat.user_1_seen=True
		else:
			friend = chat.user_1
			chat.user_2_seen=True
		chat.save()
		messages = Message.objects.filter(room=chat)
		for message in messages:
			if message.to_user == my_profile:
				message.seen=True
				message.save()
		context["chat"]=chat
		context["friend"]=friend
		context["my_profile"]=my_profile
		context["messages"]=messages
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

@method_decorator(login_required,name='dispatch')
class CreateChatGroup(CreateView):
	model = ChatRoomGroup
	template_name = "chat/create.html"
	fields = ("title",)
	context_object_name = 'form'

	def get_context_data(self,*args,**kwargs):
		context = super(CreateChatGroup,self).get_context_data(**kwargs)
		me = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		# friend_users=me.friends.all()
		friend_users = [account.user for account in Account.objects.all()]
		friend_accounts=[]
		for friend in friend_users:
			friend_accounts.append(Account.objects.get(user=friend))
		context["my_profile"]=me
		context['friends']=friend_accounts
		context["count_new_msgs"] = len(Message.objects.filter(to_user=context["my_profile"],seen=False))
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

	def form_valid(self,form):
		form.save()
		admin = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		form.instance.admin = admin
		form.instance.members.add(admin)
		for i in self.request.POST.getlist('tag_user'):
			form.instance.members.add(Account.objects.get(user=User.objects.get(username=i)))

		return super(CreateChatGroup,self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy("chat:chat_home")

@method_decorator(login_required,name='dispatch')
class GroupChat(ThemeMixin,DetailView):
	model = ChatRoomGroup
	template_name = "chat/group_chat.html"

	def get(self,request,*args,**kwargs):
		chat = ChatRoomGroup.objects.get(id=kwargs.get("pk"))
		mp = Account.objects.get(user=request.user)
		if mp not in chat.members.all():
			return HttpResponse("Permission denied!")
		else:
			return render(request,self.template_name,{"my_profile":mp,
						"group":chat,
						"messages":self.get_group_data(chat),
						"count_new_msgs":get_msgs_nots(mp),
						"new_notifications":new_notification_counter(mp.id)})

	def get_group_data(self,chat):
		return GroupMessage.objects.filter(room=chat)

@method_decorator(login_required,name='dispatch')
class Search(ListView):
	model = Account
	template_name = "chat/chat.html"
	def get(self,request,*args,**kwargs):
		query = self.request.GET.get('q')
		my_profile = Account.objects.get(user=User.objects.get(id=self.request.user.id))
		users = Account.objects.filter(Q(username__icontains=query))
		print(users)
		chat_with = []
		response_data = {"my_profile":my_profile,"count_new_msgs":len(Message.objects.filter(to_user=my_profile,seen=False))}
		if users:
			for user in users:
				filter_query = PrivateChat.objects.filter((Q(user_1=my_profile)&Q(user_2=user))|Q(user_1=user)&Q(user_2=my_profile))
				if filter_query:
					for i in PrivateChat.objects.filter((Q(user_1=my_profile)&Q(user_2=user))|Q(user_1=user)&Q(user_2=my_profile)):
						chat_with.append(i)
				else:
					chat_with.append(PrivateChat.objects.create(user_1=my_profile,user_2=user))
			print(chat_with)
			response_data.update({"chat_with":chat_with})

		return render(request,"chat/messanger.html",response_data)

@method_decorator(login_required,name='dispatch')
class ChatSettings(View,SingleObjectMixin):
	template_name = "chat/settings.html"
	model = ChatRoomGroup

	def get(self,request,*args,**kwargs):
		group = ChatRoomGroup.objects.get(pk=kwargs.get("pk"))
		return render(request,self.template_name,{"my_profile":Account.objects.get(user=User.objects.get(id=self.request.user.id)),"group":group})

@method_decorator(login_required,name='dispatch')
class GroupSettingsAddNewMembers(UpdateView):
	template_name = "chat/group_view_all_members.html"
	model = ChatRoomGroup
	fields = ("members",)

	def get(self,*args,**kwargs):
		room = ChatRoomGroup.objects.get(id=kwargs.get("pk"))
		if room.admin != Account.objects.get(user=self.request.user):
			return HttpResponse("Permission denied!")
		else:
			self.object = self.get_object()
			return super(GroupSettingsAddNewMembers,self).get(self.request,*args,**kwargs)

	def get_context_data(self,*args,**kwargs):
		context=super(GroupSettingsAddNewMembers,self).get_context_data(**kwargs)
		context["my_profile"]=Account.objects.get(user=self.request.user)
		context["count_new_msgs"] = get_msgs_nots(context["my_profile"])
		context["new_notifications"] = new_notification_counter(context["my_profile"].id)
		return context

	def post(self,request,*args,**kwargs):
		chat_room = ChatRoomGroup.objects.get(pk=kwargs.get("pk"))
		for i in request.POST.getlist("members"):
			chat_room.members.add(Account.objects.get(id=i))
		chat_room.save()
		return redirect(request.META["HTTP_REFERER"])

	def get_success_url(self):
		return reverse_lazy("chat:add_new_members")

@method_decorator(login_required,name="dispatch")
class GroupViewAllMembers(SingleObjectMixin,View):
	model = ChatRoomGroup
	template_name = "chat/group_remove_member.html"

	def get(self,request,*args,**kwargs):
		my_profile = Account.objects.get(user=request.user)
		if my_profile not in ChatRoomGroup.objects.get(id=kwargs.get("pk")).members.all():
			return HttpResponse("Permission denied!")
		else:
			self.object = self.get_object()
			group_members = self.object.members.all()
			return render(request,self.template_name,{"group_members":group_members,"my_profile":my_profile})

@method_decorator(login_required,name='dispatch')
class GroupSettingsRemoveMemberList(View):
	template_name = "chat/group_remove_member.html"

	def get(self,request,*args,**kwargs):
		user = Account.objects.get(user=User.objects.get(id=request.user.id))
		group_chat = ChatRoomGroup.objects.get(pk=kwargs.get("pk"))
		if group_chat.admin != user:
			return HttpResponse("Permission denied!")
		group_members = group_chat.members.all()
		filterd_group_members = []
		for i in range(len(group_members)):
			if group_members[i]==user:
				continue
			filterd_group_members.append(group_members[i])
		context_data = {"my_profile":user,"group_members":filterd_group_members,"group":group_chat}
		return render(request,self.template_name,context_data)

@method_decorator(login_required,name='dispatch')
class GroupSettingsRemoveMember(View):
	def get(self,request,*args,**kwargs):
		rm_user = Account.objects.get(id=kwargs.get("pk_2"))
		context_data = {"my_profile":Account.objects.get(user=request.user),"rm_user":rm_user}
		return render(request,"chat/rm_member_confirm.html",context_data)

	def post(self,request,*args,**kwargs):
		chat_group = ChatRoomGroup.objects.get(id=kwargs.get("pk_1"))
		rm_user = Account.objects.get(id=kwargs.get("pk_2"))
		chat_group.members.remove(rm_user)
		return redirect("chat:group_remove_members",pk=chat_group.id)

@method_decorator(login_required,name='dispatch')
class LeaveGroup(View):
	template_name = "chat/leave_group.html"

	def post(self,request,*args,**kwargs):
		group_id = kwargs.get("pk")
		my_profile = Account.objects.get(user=request.user)
		room = self.group_data(group_id)
		room.members.remove(my_profile)
		if room.admin == my_profile and len(room.members.all())>0:
			room.admin = room.members.first()
			room.save()
		elif room.admin == my_profile and len(room.members.all())==0:
			room.delete()
		return redirect("chat:chat_home")

	def get(self,request,*args,**kwargs):
		return render(request,self.template_name,{"group":self.group_data(kwargs.get("pk")),"my_profile":Account.objects.get(user=request.user)})

	def group_data(self,pk):
		return ChatRoomGroup.objects.get(id=pk)
