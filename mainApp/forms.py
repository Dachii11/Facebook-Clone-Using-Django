from .models import Feelings
from django import forms

class FeelingsForm(forms.ModelForm):
    class Meta:
        model = Feelings
        fields = ['feeling']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields[0].help_text = ""
            self.fields[0].label = ''
         