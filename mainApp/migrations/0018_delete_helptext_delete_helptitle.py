# Generated by Django 4.2.2 on 2023-11-06 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0017_alter_logs_ip_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HelpText',
        ),
        migrations.DeleteModel(
            name='HelpTitle',
        ),
    ]