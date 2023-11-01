from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
	path("detail/<str:pk>/",views.PostDetail.as_view(),name='post_detail'),
	path("shared/<str:pk>/",views.SharedPostDetail.as_view(),name="shared_post_detail"),
	path("g/<str:pk>/",views.GroupPostDetail.as_view(),name="group_post_detail"),
	path("gs/<str:pk>/",views.Group_shared_post_detail.as_view(),name="group_shared_post_detail"),
	path("f-detail/<str:pk>/",views.FeelingPostDetail.as_view(),name="feeling_post_detail"),
	path("fs-detail/<str:pk>/",views.FeelingPostSharedDetail.as_view(),name="feeling_post_shared_detail"),
	path("f/<str:pk>/",views.FeelingPostShare.as_view(),name="feeling_post_share"),

	path("delete/<str:pk>/",views.DeletePost.as_view(),name='delete_post'),
	path("delete/shared/<str:pk>/",views.DeleteSharedPost.as_view(),name="shared_delete_post"),
	path("delete/gs/<str:pk>/",views.DeleteGroupSharedPost.as_view(),name="delete_shared_group_post"),
	path("delete/g/<str:pk>/",views.DeleteGroupPost.as_view(),name="delete_group_post"),
	
	path("delete/feeling/<str:pk>/",views.DeleteFeelingPost.as_view(),name="delete_feeling_post"),
	path("delete/shared/feeling/<str:pk>/",views.DeleteSharedFeelingPost.as_view(),name="delete_shared_feeling_post"),

	path("share/<str:pk>/",views.Share_Post.as_view(),name="share"),
	path("add/",views.AddPost.as_view(),name="add_post"),
	path("share-group-post/<str:pk>/",views.ShareGroupPost.as_view(),name="share_group_post"),

	path("watch",views.Watch.as_view(),name='watch'),
	path("saved",views.Saves.as_view(),name="saves"),
]

