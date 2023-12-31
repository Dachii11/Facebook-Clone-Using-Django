# Generated by Django 4.2.2 on 2023-09-24 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_alter_savedposts_post_id'),
        ('accounts', '0046_rename_whoc_can_send_me_friend_request_account_who_can_send_me_friend_request'),
        ('notifications', '0004_rename_comment_commentnotifications_post_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharedPostNotifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.sharepost')),
                ('shared_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]
