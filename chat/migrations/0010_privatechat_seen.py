# Generated by Django 4.2.2 on 2023-09-29 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_message_seen'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatechat',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]
