# Generated by Django 4.2 on 2023-05-02 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('public', 'public'), ('private', 'private')], max_length=7, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.IntegerField()),
                ('profile_img', models.ImageField(default='default_profile.png', upload_to='profile_images')),
                ('cover_img', models.ImageField(default='default_cover.jpg', upload_to='backgrokund_images')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=6, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
