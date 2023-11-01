import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message,PrivateChat,GroupMessage,ChatRoomGroup
from django.contrib.auth.models import User
from accounts.models import Account
from datetime import datetime
from stories.models import Story
from operator import attrgetter
from notifications.models import *
from notifications.views import new_notification_counter

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope["url_route"]["kwargs"]["chat"]
		await self.channel_layer.group_add(
			self.room_name,
			self.channel_name
		)
		await self.accept()

	async def disconnect(self,code):
		await self.channel_layer.group_discard(
			self.room_name,
			self.channel_name
		)

	async def receive(self,text_data):
		data = json.loads(text_data)
		if "story_id" in data:
			await self.view_story(data['story_id'],data['my_profile'])
		elif "ask_for_new_message" in data and "message" in data:
			new_msg = data["ask_for_new_message"]

			if "group_id" in data:
				message = data['message']
				my_profile = data['my_profile']
				group_id= data['group_id']
				sender = data["sender"]

				await self.group_msg_save(group_id,sender,message)
				await self.channel_layer.group_send(
					self.room_name,
					{
						"type": "chat.message",
						'message':message,
						'my_profile':my_profile,
						# "new_msg":new_msg,
						'group_id':group_id,
						'sender':sender
					}	
				)
			else:	
				message = data['message']
				my_profile = data['my_profile']
				friend = data['friend']
				chat_id = data['chat_id']
				sender = data['sender']
			
				await self.message_save(chat_id,my_profile,friend,message)
				await self.channel_layer.group_send(
					self.room_name,
					{
						"type": "chat.message",
						'message':message,
						# "new_msg":new_msg,
						'my_profile':my_profile,
						'friend':friend,
						'chat_id':chat_id,
						'sender':sender
					}	
				)

		elif "ask_for_new_message" in data:	
			new_msg = data["ask_for_new_message"]
			my_profile = data["my_profile"]

			await self.channel_layer.group_send(
				self.room_name,
					{
						"type":"chat.message",
						"ask_for_new_message":new_msg,
						"new_msg":new_msg,
						"my_profile":my_profile,
					}	
			)
		else:	
			if "group_id" in data:
				message = data['message']
				my_profile = data['my_profile']
				group_id= data['group_id']
				sender = data["sender"]

				await self.group_msg_save(group_id,sender,message)
				await self.channel_layer.group_send(
					self.room_name,
					{
						"type": "chat.message",
						'message':message,
						# "new_msg":new_msg,
						'my_profile':my_profile,
						'group_id':group_id,
						'sender':sender
					}	
				)
			else:	
				message = data['message']
				my_profile = data['my_profile']
				friend = data['friend']
				chat_id = data['chat_id']
				sender = data['sender']
			
				await self.message_save(chat_id,my_profile,friend,message)
				await self.channel_layer.group_send(
					self.room_name,
					{
						"type": "chat.message",
						'message':message,
						'my_profile':my_profile,
						# "new_msg":new_msg,
						'friend':friend,
						'chat_id':chat_id,
						'sender':sender
					}	
				)

	async def chat_message(self,event):
		my_profile = event['my_profile']
		if "ask_for_new_message" in event and "message" in event:
			if not "group_id" in event:
				friend = event['friend']
				chat_id = event['chat_id']

				await self.send(text_data=json.dumps({
					#'message':message,
					'new_notification':await self.get_notifications_data(event["my_profile"]),
					'new_notification_count':await self.new_notification_count(event["my_profile"]),
					'my_profile':my_profile,
					'friend':friend,
					'my_profile_img':await self.get_my_img(my_profile),
					'time':await self.get_time(),
					'my_username':await self.get_my_username(my_profile),
					'sender':sender
				}))
			else:
				group_id = event['group_id']	
				await self.send(text_data=json.dumps({
					#'message':message,
					'my_profile':my_profile,
					'new_notification':await self.get_notifications_data(event["my_profile"]),
					'new_notification_count':await self.new_notification_count(event["my_profile"]),
					'my_profile_img':await self.get_my_img(my_profile),
					'time':await self.get_time(),
					'my_username':await self.get_my_username(my_profile),
					'sender':sender
				}))


		elif "ask_for_new_message" in event:
			await self.send(text_data=json.dumps({
				'new_notification':await self.get_notifications_data(my_profile),
				'new_notification_count':await self.new_notification_count(event["my_profile"]),
			}))
		elif "message" in event:
			message = event['message']
			sender = event['sender']
			if not "group_id" in event:
				friend = event['friend']
				chat_id = event['chat_id']

				await self.send(text_data=json.dumps({
					'message':message,
					'my_profile':my_profile,
					'friend':friend,
					'my_profile_img':await self.get_my_img(my_profile),
					'time':await self.get_time(),
					'my_username':await self.get_my_username(my_profile),
					'sender':sender
				}))
			else:
				group_id = event['group_id']	
				await self.send(text_data=json.dumps({
					'message':message,
					'my_profile':my_profile,
					'my_profile_img':await self.get_my_img(my_profile),
					'time':await self.get_time(),
					'my_username':await self.get_my_username(my_profile),
					'sender':sender
				}))
		# await self.send(text_data=json.dumps({
		# 		'new_notification':await self.get_notifications_data(my_profile),
		# 		'new_notification_count':await self.new_notification_count(my_profile),
		# 	}))

	@sync_to_async
	def message_save(self,room,sender,receiver,message):
		room = PrivateChat.objects.get(id=room)
		from_user = Account.objects.get(user=User.objects.get(id=sender))
		to_user = Account.objects.get(user=User.objects.get(id=receiver))
		msg = Message.objects.create(room=room,from_user=from_user,to_user=to_user,message=message)
		if room.user_1==from_user and room.user_2==from_user:
			room.user_1_seen=True
			room.user_2_seen=True
		else:
			if room.user_1==from_user:
				room.user_1_seen=True
				room.user_2_seen=False
			else:
				room.user_2_seen=True
				room.user_1_seen=False
		msg.save()
		room.save()

	@sync_to_async
	def group_msg_save(self,group,sender,message):
		group = ChatRoomGroup.objects.get(id=group)
		sender = Account.objects.get(user=User.objects.get(id=sender))
		if sender in group.members.all():
			print(True)
			GroupMessage.objects.create(room=group,from_user=sender,message=message).save()

	def get_unseen_msg_counts(self,receiver):
		count = 0
		messages = Message.objects.filter(to_user=receiver)
		for message in messages:
			if message.seen==False:
				count+=1
		return count

	@sync_to_async
	def get_notifications_data(self,my_profile):
		msgs_to_me = Message.objects.filter(to_user=my_profile,seen=False)
		return len(msgs_to_me)

	@sync_to_async
	def new_notification_count(self,my_profile):
		return new_notification_counter(my_profile)

	@sync_to_async
	def get_my_img(self,me):
		user = Account.objects.get(id=me)
		return user.profile_img.url

	@sync_to_async
	def get_my_username(self,my_id):
		user = Account.objects.get(id=my_id)
		return user.user.username

	@sync_to_async
	def get_time(self):
		if len(str(datetime.now().month))==1:
			month = f"0{str(datetime.now().month)}"
		else:
			month = datetime.now().month
		return f"{datetime.now().year}-{month}-{datetime.now().day}"

	@sync_to_async
	def view_story(self,story_id,user_id):
		story = Story.objects.get(id=story_id)
		user = Account.objects.get(id=user_id)
		if user not in story.views.all():
			story.views.add(user)
