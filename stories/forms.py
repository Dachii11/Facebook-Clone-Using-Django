from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Story

class AddStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ["file"]