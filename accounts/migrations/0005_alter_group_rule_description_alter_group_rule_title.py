# Generated by Django 4.1.7 on 2023-05-03 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_memebers_group_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='rule_description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='rule_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]