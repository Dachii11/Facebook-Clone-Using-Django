from django.contrib import admin
from .models import Message,PrivateChat,ChatRoomGroup,GroupMessage
# Register your models here.
admin.site.register(Message)
admin.site.register(PrivateChat)
# admin.site.register(ChatRoomGroup)

@admin.register(ChatRoomGroup)
class AccountAdmin(admin.ModelAdmin):
	list_display = ("admin","title","members_count")

	def members_count(self,obj):
		return obj.members.count()

	members_count.short_description = "members"