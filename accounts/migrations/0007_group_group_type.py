# Generated by Django 4.1.7 on 2023-05-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_group_options_group_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='group_type',
            field=models.TextField(choices=[('General', 'General'), ('Buy and Sell', 'Buy and Sell'), ('Gaming', 'Gaming'), ('Job', 'Job'), ('Parenting', 'Parenting')], max_length=15, null=True),
        ),
    ]
