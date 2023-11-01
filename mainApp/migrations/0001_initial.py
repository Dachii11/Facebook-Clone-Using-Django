# Generated by Django 4.2.2 on 2023-09-21 12:33

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0046_rename_whoc_can_send_me_friend_request_account_who_can_send_me_friend_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=800, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='HelpText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=3000)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='help_text', to='mainApp.helptitle')),
            ],
        ),
        migrations.CreateModel(
            name='Feelings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]
