# Generated by Django 4.2.2 on 2023-09-15 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0044_account_who_can_see_my_friends_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='whoc_can_send_me_friend_request',
            field=models.CharField(choices=[('Everyone', 'Everyone'), ('Friends of Friends', 'Friends of Friends'), ('No One', 'No One')], default='Everyone', max_length=20, null=True),
        ),
    ]