from django.db import models
from django.utils import timezone
from accounts.models import Account
from posts.models import feelings_list

class HelpTitle(models.Model):
	title = models.CharField(max_length=800,null=True)
	created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title[:50]

class HelpText(models.Model):
	title = models.ForeignKey(HelpTitle,on_delete=models.CASCADE,related_name="help_text")
	text = models.TextField(max_length=3000)

	def __str__(self):
		return self.text[:50]

class Feelings(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	feeling = models.CharField(max_length=35,null=True,choices=feelings_list)
	c = (("feeling_post","feeling_post"),)
	post_type = models.CharField(max_length=15,choices=c,null=True,default="feeling_post")
	# views = models.ManyToManyField(Account,blank=True,related_name='ShareFeelingView')

	likes = models.ManyToManyField(Account,related_name='feelings_likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="feelings_like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="feelings_love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="feelings_haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='feelings_wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='feelings_sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='feelings_angry_reaction')

	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"{self.user} feels {self.feeling} today."

class ShareFeelingsPosts(models.Model):
	type_of_post = (("sharedFeelingPost","sharedFeelingPost"),)
	post_type = models.TextField(choices=type_of_post,null=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	caption = models.TextField(max_length=1500,blank=True)
	referer_post = models.ForeignKey(Feelings,on_delete=models.CASCADE,null=True,related_name='feelings_post')
	# views = models.ManyToManyField(Account,blank=True,related_name='ShareFeelingView')
	created_at = models.DateTimeField(default=timezone.now)

	likes = models.ManyToManyField(Account,related_name='shared_feeling_post_likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_feeling_post_like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_feeling_post_love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_feeling_post_haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_feeling_post_wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_feeling_post_sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_feeling_angry_reaction')

	def __str__(self):
		return f"Shared: {self.id}"


class Logs(models.Model):
	user_logged_in = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
	ip_address = models.CharField(max_length=80,null=True)
	user_agent = models.CharField(max_length=500,null=True)
	city = models.CharField(max_length=100,null=True)
	country = models.CharField(max_length=100,null=True)
	time = models.DateTimeField(default=timezone.now)