from django.contrib import admin
from .models import *

admin.site.register(PostNotifications)
admin.site.register(SharedPostNotifications)
admin.site.register(CommentNotifications)
admin.site.register(ReplyCommentNotifications)
admin.site.register(GroupInviteNotifications)