from django.contrib import admin
from django.utils.html import format_html
from .models import *

admin.site.register(FriendRequest)
admin.site.register(GroupVisitors)
admin.site.register(GroupPost)
admin.site.register(GroupRules)
admin.site.register(Report)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	list_display = ("user","gender","from_country")

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	list_display = ("group_name","privacy","visibility","members_count","admin_count")

	def members_count(self,obj):
		return format_html(f"<strong>{obj.members.count()}</strong>")
		
	def admin_count(self,obj):
		return format_html(f"<b>{obj.admin.count()}</b>")

	members_count.short_description = "members"
	admin_count.short_description = "admins"

@admin.register(GroupSharePost)
class GroupSharePostAdmin(admin.ModelAdmin):
	list_display = ("user","Caption","referer_post_id","created_at")

	def Caption(self,obj):
		if len(obj.caption[:30])>len(obj.caption):
			return f"{obj.caption[:30]}..."
		return obj.caption

	Caption.short_description = "Caption"