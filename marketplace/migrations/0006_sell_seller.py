# Generated by Django 4.2.2 on 2023-09-05 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_alter_account_who_can_see_my_posts'),
        ('marketplace', '0005_alter_sell_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell',
            name='seller',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
            preserve_default=False,
        ),
    ]
