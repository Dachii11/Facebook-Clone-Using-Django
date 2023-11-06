from django.forms import ModelForm
from .models import Comment,CommentReport

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ["text"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].label = ""
			self.fields[field].widget.attrs['placeholder'] = 'Write a comment...'
			self.fields[field].widget.attrs["class"] = 'inp'
