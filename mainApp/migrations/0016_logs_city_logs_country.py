# Generated by Django 4.2.2 on 2023-10-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_logs_user_agent'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='logs',
            name='country',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
