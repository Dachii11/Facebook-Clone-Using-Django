# Generated by Django 4.2.2 on 2023-09-22 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0046_rename_whoc_can_send_me_friend_request_account_who_can_send_me_friend_request'),
        ('mainApp', '0005_alter_feelings_feeling'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feelings',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
    ]
