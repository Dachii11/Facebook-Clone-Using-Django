# Generated by Django 4.2.2 on 2023-10-04 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_rename_whoc_can_send_me_friend_request_account_who_can_send_me_friend_request'),
        ('posts', '0017_alter_post_feeling'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='accounts.account'),
        ),
    ]