from django.db import models
from accounts.models import Account,Group
from posts.models import Post,SharePost
from comments.models import Comment,CommentReply

class PostNotifications(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user} created new post"

class SharedPostNotifications(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	shared_post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
	post = models.ForeignKey(SharePost,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user} shared {shared_post.user}'s post"

class CommentNotifications(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	post_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.user} commented on {self.post_comment.post.user}'s post"

class ReplyCommentNotifications(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
	repylied_comment = models.ForeignKey(CommentReply,on_delete=models.CASCADE,null=True)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)


	def __str__(self):
		return f"{self.user} replied on {self.comment.user}'s post"	

class GroupInviteNotifications(models.Model):
	sender = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="invite_sender",null=True)
	receiver = models.ForeignKey(Account,on_delete=models.CASCADE,related_name="invite_receiver",null=True)
	group_to_invite = models.ForeignKey(Group,on_delete=models.CASCADE,null=True)
	text = models.TextField(max_length=2500)
	date = models.DateTimeField(auto_now_add=True)
	seen = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.sender} invited {self.receiver} to {self.group_to_invite.group_name}"