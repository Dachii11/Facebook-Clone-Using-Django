from django import forms
from .models import Message,ChatRoomGroup

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['message']
	        
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

			self.fields[0].help_text = ""
			self.fields[0].label = ''

class AddGroupMemberForm(forms.ModelForm):
	class Meta:
		model = ChatRoomGroup
		fields = ["members"]