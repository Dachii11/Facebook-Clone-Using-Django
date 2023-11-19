from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Group,GroupPost,GroupRules,Report
from .models import Account
from django.forms import widgets

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200,help_text="Required")
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password1','password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields: 
            self.fields[field].help_text = "" 
            self.fields["username"].widget.attrs['placeholder'] = "Username (25 characters or fewer)"
            self.fields["email"].widget.attrs['placeholder'] = "Email"
            self.fields["password1"].widget.attrs['placeholder'] = "Password"
            self.fields["password2"].widget.attrs['placeholder'] = "Repeat Password"
            self.fields["first_name"].widget.attrs['placeholder'] = "First Name"
            self.fields["last_name"].widget.attrs['placeholder'] = "Last Name"

        for fieldname in ['username','email', 'password1', 'password2']:
            if fieldname == 'password2':
                self.fields[fieldname].help_text = "<p class='help_text'>Your password must contain at least 8 characters</p>"
                self.fields[fieldname].help_text += "<p class='help_text'>Your password can’t be entirely numeric</p>"
                self.fields[fieldname].label = ''
            elif fieldname == 'username':
                self.fields[fieldname].help_text = "Letters, digits and @/./+/-/_ only"
                self.fields[fieldname].label = ''
            else:
                self.fields[fieldname].help_text = None
                self.fields[fieldname].label = ""

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text=None
        self.fields["password"].widget = widgets.PasswordInput()

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["group_name","privacy","visibility","group_type","who_can_post","description","group_cover"]

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ["caption","file","is_anonymous"]

class RuleAddForm(forms.ModelForm):
    class Meta:
        model = GroupRules
        fields = ["rule_title","rule_body"]

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ["visibility","privacy","group_name","description","group_type","who_can_post","display_post_author_username_on_post","group_cover"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            if fieldname == 'visibility':
                self.fields[fieldname].label = 'Hide Group'
            elif fieldname == 'privacy':
                self.fields[fieldname].label = 'privacy'
            elif fieldname == 'group_name':
                self.fields[fieldname].label = "Name"
                self.fields[fieldname].widget.attrs['placeholder'] = "Group Name..."
            elif fieldname == 'description':
                self.fields[fieldname].label = "description"
                self.fields[fieldname].widget.attrs['placeholder'] = "Description..."
            elif fieldname == 'group_type':
                self.fields[fieldname].label = "Group type"
            elif fieldname == 'who_can_post':
                self.fields[fieldname].label = "Who Can Post"
            elif fieldname == "display_post_author_username_on_post":
                self.fields[fieldname].label = "Display post author username on post"


            else:
                self.fields[fieldname].help_text = None
                self.fields[fieldname].label = ""

            self.fields[fieldname].help_text=None
            self.fields[fieldname].required=False

            
class GroupReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["why","problem","text"]

class EditProfile(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["gender","profile_img","cover_img","bio","from_country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].label = ""
            self.fields[fieldname].help_text=None