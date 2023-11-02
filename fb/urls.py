from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import activate
from django.urls import re_path

urlpatterns = [ 
    path('1KDl0KL_03kffj_jKA_SF0k_l1K03_31KL_KDA/', admin.site.urls),
    path("",include("mainApp.urls")),
    path("posts/",include("posts.urls")),
    path("accounts/",include("accounts.urls")),
    path("comments/",include("comments.urls")),
    path("chat/",include("chat.urls")),
    path("notifications/",include("notifications.urls")),
    path("marketplace/",include("marketplace.urls")),
    path("stories/",include("stories.urls")),

    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path("password_change/",auth_views.PasswordChangeView.as_view(template_name="accounts/password_change.html"),name="password_change"),
    # path("password_change/",MyPasswordChangeView.as_view(),name="password_change"),
    path("password_reset/done/",auth_views.PasswordResetCompleteView.as_view(),name="password_reset_done"),
    path("password_reset/",auth_views.PasswordResetView.as_view(),name='password_reset'),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),

    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),

    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate,name='activate'),
    path("activate/<uidb64>/<token>/",activate,name='activate'),

    re_path(r"^media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),
]
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
