# Generated by Django 4.2.2 on 2023-09-06 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_alter_account_who_can_see_my_posts'),
        ('marketplace', '0008_remove_sell_total_views_sell_total_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sell',
            name='total_views',
        ),
        migrations.AddField(
            model_name='sell',
            name='total_views',
            field=models.ManyToManyField(related_name='total_views', to='accounts.account'),
        ),
    ]
