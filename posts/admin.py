from django.contrib import admin
from .models import Post,SharePost,SavedPosts

admin.site.register(Post)
admin.site.register(SharePost)
admin.site.register(SavedPosts)