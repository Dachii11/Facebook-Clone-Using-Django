from django.db import models
import uuid
from accounts.models import Account
from mimetypes import guess_type
from django.utils import timezone
from django.contrib.auth import get_user_model
from mainApp.number_format import human_format,get_letter_for_number_format

feelings_list = (
	("accomplished","accomplished"),("aggravated","aggravated"),("alive","alive"),("alone","alone"),
	("amazed","amazed"),("amazing","amazing"),("amused","amused"),("angry","angry"),("annoyed","annoyed"),
	("anxious","anxious"),("awesome","awesome"),("awful","awful"),("bad","bad"),("beautiful","beautiful"),
	("better","better"),("blah","blah"),("blessed","blessed"),("bored","bored"),("broken","broken"),
	("chill","chill"),("cold","cold"),("comfortable","comfortable"),("confident","confident"),("confused","confused"),
	("content","content"),("cool","cool"),("crappy","crappy"),("crazy","crazy"),("curios","curios"),
	("depressed","depressed"),("determined","determined"),("disappointed","disappointed"),("down","down"),
	("drained","drained"),("drunk","drunk"),("ecstatic","ecstatic"),("emotional","emotional"),
	("energized","energized"),("excited","excited"),("fantastic","fantastic"),("fat","fat"),("free","free"),
	("fresh","fresh"),("frustrated","frustrated"),("full","full"),("funny","funny"),("good","good"),("grateful","grateful"),
	("great","great"),("guilty","guilty"),("happy","happy"),("heartbroken","heartbroken"),("helpless","helpless"),
	("hopeless","hopeless"),("hopeful","hopeful"),("hopeless","hopeless"),("horrible","horrible"),("hot","hot"),
	("hungry","hungry"),("horny","horny"),("hurt","hurt"),("impatient","impatient"),("in love","in love"),("incomplete","incomplete"),
	("inspired","inspired"),("irritated","irritated"),("lazy","lazy"),("lonely","lonely"),("lost","lost"),
	("loved","loved"),("lovely","lovely"),("lucky","lucky"),("mad","mad"),("meh","meh"),("miserable","miserable"),
	("motivated","motivated"),("nervous","nervous"),("nostalgic","nostalgic"),("OK","OK"),("old","old"),
	("optimistic","optimistic"),("overwhelmed","overwhelmed"),("pained","pained"),("pissed","pissed"),
	("pissed off","pissed off"),("positive","positive"),("pretty","pretty"),("proud","proud"),("pumped","pumped"),
	("ready","ready"),("refreshed","refreshed"),("relaxed","relaxed"),("relieved","relieved"),("rough","rough"),
	("sad","sad"),("safe","safe"),("satisfied","satisfied"),("scared","scared"),("sexy","sexy"),("shocked","shocked"),
	("sick","sick"),("silly","silly"),("sleepy","sleepy"),("sore","sore"),("sorry","sorry"),("special","special"),
	("stressed","stressed"),("strong","strong"),("stupid","stupid"),("super","super"),("surprised","surprised"),
	("terrible","terrible"),("thankful","thankful"),("tired","tired"),("uncomfortable","uncomfortable"),
	("upset","upset"),("weak","weak"),("weird","weird"),("well","well"),("wonderfull","wonderfull"),("worried","worried")
)
class Post(models.Model):
	def location_data():
		countries = []
		with open("mainApp/countries.txt","r") as f:
			for i in f.readlines():
				i=i.replace('\n','')
				countries.append((i,i))
		return tuple(countries)

	type_of_post = (("post","post"),)
	post_type = models.TextField(choices=type_of_post,null=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	file = models.FileField(upload_to="PostsIcons",blank=True)
	caption = models.TextField(max_length=1500,blank=True)
	tag_users = models.ManyToManyField(Account,blank=True,related_name='tag_users')
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(Account,related_name='likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='angry_reaction')
	views = models.ManyToManyField(Account,blank=True,related_name='views')

	statuses = (
			("Public","Public"),
			("Private","Private"),
			("Friends","Friends"),
		)
	status = models.CharField(choices=statuses,null=True,max_length=8,default="Public")
	tags = models.ManyToManyField(Account,related_name="tags",blank=True)
	location = models.CharField(choices=location_data(),max_length=40,blank=True)
	feeling = models.CharField(choices=feelings_list,max_length=40,null=True,blank=True)

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
     
	def hf(self):
		c = len(self.likes.all())
		return human_format(c)[0]

	def glf(self):
		return get_letter_for_number_format(human_format(len(self.likes.all()))[1])

	def glsp(self):
		return get_letter_for_number_format(human_format(self.count_shares(self))[1])

	def mcu(self):
		num = float('{:.3g}'.format(len(self.likes.all())-1))
		magnitude = 0
		while abs(num)>=1000:
				magnitude += 1
				num /= 1000.0
		return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),['','K','M','B','T'][magnitude])

	def count_shares(self,post):
		return len(SharePost.objects.filter(referer_post=post))
	
	def get_formated_shares(self):
		return human_format(self.count_shares(self))[0]

	def __str__(self):
		return f"Post: {self.id}"

class SharePost(models.Model):
	type_of_post = (("shared","shared"),)
	post_type = models.TextField(choices=type_of_post,null=True)
	user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
	caption = models.TextField(max_length=1500,blank=True)
	referer_post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,related_name='shares')
	views = models.ManyToManyField(Account,blank=True,related_name='SharePostView')
	created_at = models.DateTimeField(default=timezone.now)

	likes = models.ManyToManyField(Account,related_name='shared_post_likes',blank=True)
	like_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_post_like_reaction")
	love_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_post_love_reaction")
	haha_reaction = models.ManyToManyField(Account,blank=True,related_name="shared_post_haha_reaction")
	wow_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_post_wow_reaction')
	sad_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_post_sad_reaction')
	angry_reaction = models.ManyToManyField(Account,blank=True,related_name='shared_post_angry_reaction')
	statuses = (("Public","Public"),("Private","Private"),("Friends","Friends"))
	status = models.CharField(choices=statuses,null=True,max_length=8,default="Public")
	tags = models.ManyToManyField(Account,related_name="shared_tags",blank=True)

	def hf(self):
		c = len(self.likes.all())
		return human_format(c)[0]

	def glf(self):
		return get_letter_for_number_format(human_format(len(self.likes.all()))[1])

	def mcu(self):
		num = float('{:.3g}'.format(len(self.likes.all())-1))
		magnitude = 0
		while abs(num)>=1000:
				magnitude += 1
				num /= 1000.0
		return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),['','K','M','B','T'][magnitude])

class SavedPosts(models.Model):
	user = models.ForeignKey(Account,on_delete=models.CASCADE)
	post_type = models.CharField(max_length=50)
	post_id = models.TextField(null=True)
	saved_at = models.DateTimeField(default=timezone.now)
