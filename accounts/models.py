from django.db import models
from django.db.models import fields
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from mimetypes import guess_type
from chat.models import PrivateChat
from django.contrib.auth.base_user import BaseUserManager
from django import template

class Account(models.Model):
	genders = (("male","male"),("female","female"))
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	username = models.CharField(max_length=300,null=True)
	id_user = models.IntegerField()
	profile_img = models.ImageField(upload_to='profile_images',default="default_profile.png")
	cover_img = models.ImageField(upload_to='backgrokund_images',default="default_cover.png")
	gender = models.CharField(max_length=6,choices=genders,null=True,default='male')
	friends = models.ManyToManyField(User,blank=True,related_name='friends')
	bio = models.TextField(max_length=500,blank=True)
	from_country = models.CharField(max_length=50)
	theme = models.BooleanField(default=True)

	who_can_see_my_posts_choices = (
			("Public","Public"),
			("Friends","Friends"),
			("Only me","Only me"),
		)
	who_can_see_my_friends_list_choices = (
			("Everyone","Everyone"),
			("Friends","Friends"),
			("Only Me","Only Me"),
		)
	whoc_can_send_me_friend_request_choices = (
			("Everyone","Everyone"),
			("Friends of Friends","Friends of Friends"),
			("No One","No One"),
		)
	who_can_see_my_posts = models.CharField(max_length=10,choices=who_can_see_my_posts_choices,default="Public",null=True)
	who_can_see_my_email_address = models.CharField(max_length=10,choices=who_can_see_my_friends_list_choices,default="Everyone",null=True)
	who_can_see_my_friends_list = models.CharField(max_length=10,choices=who_can_see_my_friends_list_choices,default="Everyone",null=True)
	who_can_send_me_friend_request = models.CharField(max_length=20,choices=whoc_can_send_me_friend_request_choices,default="Everyone",null=True)
	
	def __str__(self):
		return self.user.username


class FriendRequest(models.Model):
    from_user = models.ForeignKey(Account,related_name='from_user',on_delete=models.CASCADE)
    to_user = models.ForeignKey(Account,related_name="to_user",on_delete=models.CASCADE)
    sent_on = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.from_user.user} send request to {self.to_user.user}"
    
class Group(models.Model):
	statuses = (("Public","Public"),("Private","Private"))
	visible = (("Visible","Visible"),("Hidden","Hidden"))
	types = (("General","General"),("Buy and Sell","Buy and Sell"),("Gaming","Gaming"),
			 ("Job","Job"),("Parenting","Parenting"))
	privacy = models.CharField(max_length=7,choices=statuses,null=True)
	admin = models.ManyToManyField(Account)
	visibility = models.CharField(max_length=7,choices=visible,null=True)
	group_name = models.CharField(max_length=70,unique=True,null=True)
	group_cover = models.ImageField(upload_to="group_covers",default="default_cover.png")
	members = models.ManyToManyField(Account,related_name="members",blank=True)
	description = models.TextField(max_length=1000,null=True,blank=True)
	
	group_type = models.TextField(max_length=15,choices=types,null=True)
	who_can_post_list = (("Only Admins","Only Admins"),("Everyone","Everyone"))
	who_can_post = models.CharField(max_length=15,choices=who_can_post_list,default="Everyone")

	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.group_name

	class Meta:
		ordering = ['-created']

	

class GroupRules(models.Model):
	group = models.ForeignKey(Group,on_delete=models.CASCADE)
	rule_title = models.CharField(max_length=500)
	rule_body = models.TextField(max_length=5000)

	def __str__(self):
		return self.rule_title
	
class GroupVisitors(models.Model):
	visitor = models.ForeignKey(Account,on_delete=models.CASCADE)
	group = models.ForeignKey(Group,on_delete=models.CASCADE)
	count = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.visitor} visits group '{self.group.group_name}' {self.count} times"
		
class GroupPost(models.Model):
	group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,related_name='posts')
	type_of_post = (("groupPost","groupPost"),)
	post_type = models.TextField(choices=type_of_post,null=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	caption = models.TextField(max_length=3000,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to="GroupPostsIcons",blank=True)

	is_anonymous = models.BooleanField(default=False)
	likes = models.ManyToManyField(Account,related_name='group_post_likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="group_post_like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="group_post_love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="group_post_haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='group_post_wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='group_post_sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='group_post_angry_reaction')
	views = models.ManyToManyField(Account,blank=True,related_name='group_views')

	class Meta:
		ordering = ['-created_at']

	def media_type_html(self):
		if self.file!="":
		    type_tuple = guess_type(self.file.url, strict=True)
		    if (type_tuple[0]).__contains__("image"):
		        return "image"
		    elif (type_tuple[0]).__contains__("video"):
		        return "video"
		else:
			return "none"
	def __str__(self):
		return f"Group Post: {self.id}"

class GroupSharePost(models.Model):
	type_of_post = (("groupShared","groupShared"),)
	post_type = models.TextField(choices=type_of_post,null=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	caption = models.TextField(max_length=1500,blank=True)
	referer_post = models.ForeignKey(GroupPost,on_delete=models.CASCADE,null=True,related_name='group_shares')
	views = models.ManyToManyField(Account,blank=True,related_name='groupSharePostView')
	created_at = models.DateTimeField(default=timezone.now)

	likes = models.ManyToManyField(Account,related_name='group_shared_post_likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="group_shared_post_like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="group_shared_post_love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="group_shared_post_haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='group_shared_post_wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='group_shared_post_sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='group_shared_post_angry_reaction')


class Report(models.Model):

	what_happening = (("Hate speech","Hate speech"),("Nudity or sexual content","Nudity or sexual content"),("Violence","Violence"),("Harassment","Harassment"),
						("Scams and fake Groups","Scams and fake Groups"),("Unauthorised sales","Unauthorised sales"),("intellectual property","intellectual property"))
	understand_problem = (("Asking for financial information","Asking for financial information"),("Pretending to be another business","Pretending to be another business"),
						("Pretending to be another person","Pretending to be another person"),("Fake Groups","Fake Groups"),("Misleading Group name change","Misleading Group name change"))

	report_group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True)
	who_reported = models.ForeignKey(Account,on_delete=models.CASCADE)
	why = models.TextField(choices=what_happening,max_length=35,null=True)
	problem = models.TextField(choices=understand_problem,max_length=35,null=True,blank=True)
	text = models.TextField(max_length=5000,null=True,blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.who_reported.username} reported '{self.report_group.group_name}'"