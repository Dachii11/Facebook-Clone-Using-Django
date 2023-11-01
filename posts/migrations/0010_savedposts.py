# Generated by Django 4.1.7 on 2023-06-07 11:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0029_groupvisitors'),
        ('posts', '0009_alter_sharepost_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(max_length=50)),
                ('post_id', models.TextField()),
                ('saved_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
    ]