# Generated by Django 4.2.2 on 2023-08-17 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='who_reported',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
            preserve_default=False,
        ),
    ]