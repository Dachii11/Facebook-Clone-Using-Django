# Generated by Django 4.2.2 on 2023-09-15 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0005_story_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-time']},
        ),
    ]
