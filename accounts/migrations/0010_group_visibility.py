# Generated by Django 4.1.7 on 2023-05-04 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_group_group_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='visibility',
            field=models.CharField(choices=[('public', 'public'), ('hidden', 'hidden')], max_length=6, null=True),
        ),
    ]
