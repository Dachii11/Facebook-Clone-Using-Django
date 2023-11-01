from django.db import models
import accounts.models

class PrivateChat(models.Model):
    user_1 = models.ForeignKey("accounts.Account",on_delete=models.CASCADE,related_name='user_1')
    user_2 = models.ForeignKey("accounts.Account",on_delete=models.CASCADE,related_name='user_2')
    user_1_seen = models.BooleanField(default=False)
    user_2_seen = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user_1} - {self.user_2} conversation"

class Message(models.Model):
	room = models.ForeignKey(PrivateChat,on_delete=models.CASCADE,null=True,related_name="messages")
	from_user = models.ForeignKey("accounts.Account",on_delete=models.CASCADE,related_name='sender')
	to_user = models.ForeignKey("accounts.Account",on_delete=models.CASCADE,related_name="recevier")
	message = models.TextField()
	seen = models.BooleanField(default=False)
	date_send = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	 	return f"{self.from_user} to {self.to_user}: {self.message[:50]}"

class ChatRoomGroup(models.Model):
	admin = models.ForeignKey("accounts.Account",on_delete=models.SET_NULL,null=True)
	members = models.ManyToManyField("accounts.Account",related_name='memsbers')
	title = models.CharField(max_length=40)
	icon = models.ImageField(upload_to="group_chat_covers",default="default_cover.png")
	created = models.DateTimeField(auto_now_add=True)

class GroupMessage(models.Model):
	room = models.ForeignKey(ChatRoomGroup,on_delete=models.CASCADE,null=True,related_name="group_messages")
	from_user = models.ForeignKey("accounts.Account",on_delete=models.CASCADE,related_name='msg_sender')
	message = models.TextField()
	date_send = models.DateTimeField(auto_now_add=True)

	def __str__(self):
	 	return f"{self.from_user} io {self.room.title}: {self.message[:50]}"