# Generated by Django 4.2.2 on 2023-10-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_sharepost_status_sharepost_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='feeling',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
