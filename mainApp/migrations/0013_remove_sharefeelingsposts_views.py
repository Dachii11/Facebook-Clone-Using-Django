# Generated by Django 4.2.2 on 2023-09-23 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0012_sharefeelingsposts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharefeelingsposts',
            name='views',
        ),
    ]
