# Generated by Django 4.2.2 on 2023-09-13 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_alter_story_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
