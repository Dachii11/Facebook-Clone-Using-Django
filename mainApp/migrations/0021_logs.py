# Generated by Django 4.2.2 on 2023-11-27 10:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0054_group_blue_tick'),
        ('mainApp', '0020_rename_logs_loggin_logs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=80, null=True)),
                ('method_type', models.CharField(max_length=50, null=True)),
                ('method', models.CharField(max_length=200, null=True)),
                ('status_code', models.CharField(max_length=10, null=True)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.account')),
            ],
        ),
    ]
