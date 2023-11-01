from django.contrib import admin
from .models import HelpTitle,HelpText,Feelings,ShareFeelingsPosts
# Register your models here.
admin.site.register(HelpTitle)
admin.site.register(HelpText)
admin.site.register(Feelings)
admin.site.register(ShareFeelingsPosts)