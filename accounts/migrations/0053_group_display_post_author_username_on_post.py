# Generated by Django 4.2.2 on 2023-11-19 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0052_alter_group_group_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='display_post_author_username_on_post',
            field=models.BooleanField(default=False),
        ),
    ]
