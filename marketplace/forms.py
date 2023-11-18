from django import forms
from .models import Sell

class AddProductForm(forms.ModelForm):
	class Meta:
		model = Sell
		fields = ["name","image","category","price","description"]