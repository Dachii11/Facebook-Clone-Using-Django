# Generated by Django 4.1.7 on 2023-05-11 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_groupsharepost_group'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='status',
            new_name='privacy',
        ),
    ]