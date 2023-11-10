from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

app_name = 'accounts'
urlpatterns = [
	path("profile/<str:pk>/",views.Profile.as_view(),name='profile'),
	path("group/<str:pk>/",views.GroupDetail.as_view(),name='group'),
	
	path("login/",views.SignIn.as_view(),name='login'),
	path("logout/",auth_views.LogoutView.as_view(),name='logout'),
	path("signup/",views.SignUp.as_view(),name='signup'),
	
	path("groups/",views.Groups.as_view(),name="groups"),
	path("group-create/",views.CreateGroup.as_view(),name='create_group'),

	path("suggestions/",views.Suggestions.as_view(),name='suggestions'),
	path("group/<str:pk>/add/",views.CreateGroupPost.as_view(),name='add_group_post'),

	path("requests/",views.FriendRequests.as_view(),name="friend_requests"),
	path("friends/",views.Friends.as_view(),name="friends"),

	path("group/<str:pk>/about",views.GroupAbout.as_view(),name="about"),
	path("group/<str:pk>/members",views.GroupMembers.as_view(),name='members'),

	path("group/<str:pk>/rules/",views.GroupRule.as_view(),name='group_rules'),
	path("group/<str:pk>/rule-add/",views.AddGroupRule.as_view(),name="rule-add"),
	path("group/<str:pk>/edit/",views.EditGroup.as_view(),name="edit"),

	path("group/<str:pk>/report",views.ReportGroup.as_view(),name="report_group"),

	path("settings/",views.Settings.as_view(),name="settings"),
	path("edit/",views.EditProfile.as_view(),name="edit_profile"),
	path("delete-group/<str:pk>/",views.DeleteGroup.as_view(),name="delete_group"),

	path("settings/who_can_see_my_posts/",views.WhoCanSeeMyPosts.as_view(),name='who_can_see_my_posts'),
	path("settings/who_can_see_friends_list/",views.WhoCanSeeMyFriendList.as_view(),name='who_can_see_my_friends_list'),
	path("settings/who_can_send_me_friend_request/",views.WhoCanSendMeFriendRequest.as_view(),name='who_can_send_me_friend_request'),
	path("settings/who_can_see_my_email_address/",views.WhoCanSeeMyEmailAddress.as_view(),name="who_can_see_my_email_address"),

	# path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate,name='activate'),
]

