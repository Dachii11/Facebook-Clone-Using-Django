from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
	path("create/",views.CreateChatGroup.as_view(),name="create"),
	path("search/",views.Search.as_view(),name="search"),
	path("group-settings/<str:pk>/",views.ChatSettings.as_view(),name="settings"),
	path("members/<str:pk>/",views.GroupSettingsAddNewMembers.as_view(),name="add_new_members"),
	path("remove/<str:pk>/",views.GroupSettingsRemoveMemberList.as_view(),name="group_remove_members"),
	path("view/<str:pk>/",views.GroupViewAllMembers.as_view(),name="view_all_members"),
	path("del/<str:pk_1>/<str:pk_2>/",views.GroupSettingsRemoveMember.as_view(),name="rm_member"),
	path("leave/<str:pk>/",views.LeaveGroup.as_view(),name="leave_group"),
	path("<str:pk>/",views.Chat.as_view(),name='chat'),
	path("group/<str:pk>/",views.GroupChat.as_view(),name="group_chat"),
	path("messanger/<str:pk>/",views.Redirect.as_view(),name='detail'),
	path("",views.ChatHome.as_view(),name="chat_home"),
]