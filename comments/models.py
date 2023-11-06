from django.db import models
from posts.models import Post,SharePost
from accounts.models import GroupPost,GroupSharePost
from accounts.models import Account
import uuid
from django.utils import timezone
from mainApp.models import Feelings,ShareFeelingsPosts

class Comment(models.Model):
	comment_types = (
			("PostComment","PostComment"),
			("SharedPostComment","SharedPostComment"),
			("GroupSharedPostComment","GroupSharedPostComment"),
			("GroupPostComment","GroupPostComment"),
			("FeelingPostComment","FeelingPostComment"),
			("FeelingSharedPostComment","FeelingSharedPostComment"))

	id = models.UUIDField(primary_key=True,default=uuid.uuid4)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	text = models.CharField(max_length=1000,blank=True)
	created = models.DateTimeField(default=timezone.now)
	type_of_comment = models.CharField(max_length=30,choices=comment_types,null=True)
	likes = models.ManyToManyField(Account,related_name='commlikes')

	post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name='comments')
	share_post = models.ForeignKey(SharePost,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name='shared_post_comments')
	group_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name="group_post_comment")
	group_shared_post = models.ForeignKey(GroupSharePost,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name="group_shared_post")
	feeling_post = models.ForeignKey(Feelings,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name="feeling_post")
	feeling_shared_post = models.ForeignKey(ShareFeelingsPosts,on_delete=models.CASCADE,null=True,default=None,blank=True,related_name="feeling_share_post")
	
	def __str__(self):
		return self.text[:50]

class CommentReply(models.Model):
	comment_reply_types = (
			("PostCommentsReply","PostCommentsReply"),
			("SharedPostCommentReply","SharedPostCommentReply"),
			("GroupPostCommentReply","GroupPostCommentReply"),
			("SharedGroupPostCommentReply","SharedGroupPostCommentReply"),
			("FeelingPostCommentReply","FeelingPostCommentReply"))

	parrent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name='reply')

	reply_type = models.CharField(max_length=30,choices=comment_reply_types,null=True)
	id = models.UUIDField(primary_key=True,default=uuid.uuid4)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	text = models.CharField(max_length=1000,blank=True)
	likes = models.ManyToManyField(Account,related_name='replylikes')
	created = models.DateTimeField(default=timezone.now)
	class Meta:
		ordering = ['-created']

	def __str__(self):
		return self.text[:50]

class CommentReport(models.Model):
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
	reasons = (
			("Nudity","Nudity"),
			("Violence","Violence"),
			("Harassment","Harassment"),
			("Suicide or Self-injury","Suicide or Self-injury"),
			("Spam","Spam"),
			("Unauthorized Sales","Unauthorized Sales"),
			("Hate Speech","Hate Speech"),
			("Terrorism","Terrorism"),
			("Something Else","Something Else"),
		)
	text = models.TextField(max_length=1500,null=True)
	reason = models.CharField(max_length=50,choices=reasons,default="Nudity")
	user_who_reports = models.ForeignKey(Account,on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.user_who_reports.username} reported {self.comment.user.username}'s Comment."
