# Generated by Django 4.2.2 on 2023-10-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0016_logs_city_logs_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logs',
            name='ip_address',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
