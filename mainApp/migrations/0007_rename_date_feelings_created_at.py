# Generated by Django 4.2.2 on 2023-09-22 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_alter_feelings_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feelings',
            old_name='date',
            new_name='created_at',
        ),
    ]
