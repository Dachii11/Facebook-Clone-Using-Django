# Generated by Django 4.2.2 on 2023-08-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_alter_report_who_reported'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='text',
            field=models.TextField(max_length=5000, null=True),
        ),
    ]