# Generated by Django 4.2.2 on 2023-08-31 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0041_account_from_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='who_can_see_my_posts',
            field=models.CharField(choices=[('Public', 'Public'), ('Friends', 'Friends'), ('Only me', 'Only me')], max_length=10, null=True),
        ),
    ]
