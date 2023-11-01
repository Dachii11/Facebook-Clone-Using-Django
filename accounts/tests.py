from django.test import TestCase
from accounts.models import *
from django.contrib.auth.models import User

class AccountTest(TestCase):
	def setUp(self):
		user = User.objects.create(username="Username",email="email@gmail.com",password1="pass1",password2="pass2")
		Account.objects.create(gender="male",user=user,id_user=user.id)
		Account.objects.create(gender="male",user=user)

class FriendRequestTest(TestCase):
	def setUp(self):
		user = User.objects.create(username="Username",email="email@gmail.com",password1="pass1",password2="pass2")
		u1=Account.objects.create(gender="female",user=user,id_user=user.id)
		u2=Account.objects.create(gender="male",user=user,id_user=user.id)

		FriendRequest.objects.create(from_user=u1,to_user=u1)


class GroupTest(TestCase):
	def setUp(self):
		user = User.objects.create(username="Username",email="email@gmail.com",password1="pass1",password2="pass2")
		u1=Account.objects.create(gender="female",user=user,id_user=user.id)

		FriendRequest.objects.create(from_user=u1,to_user=u1)
		Group.objects.create(privacy="Public",admin=u1,visibility="Visible",group_name="name",group_type="General")