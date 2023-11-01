# Generated by Django 4.2.2 on 2023-10-07 12:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_rename_whoc_can_send_me_friend_request_account_who_can_send_me_friend_request'),
        ('mainApp', '0013_remove_sharefeelingsposts_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=20, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_logged_in', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.account')),
            ],
        ),
    ]
