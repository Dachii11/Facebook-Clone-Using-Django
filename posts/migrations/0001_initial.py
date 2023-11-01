# Generated by Django 4.2 on 2023-05-02 18:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.TextField(choices=[('post', 'post')], null=True)),
                ('file', models.FileField(blank=True, upload_to='PostsIcons')),
                ('caption', models.TextField(blank=True, max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('angry_reaction', models.ManyToManyField(blank=True, related_name='angry_reaction', to='accounts.account')),
                ('haha_reaction', models.ManyToManyField(blank=True, related_name='haha_reaction', to='accounts.account')),
                ('like_reaction', models.ManyToManyField(blank=True, related_name='like_reaction', to='accounts.account')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to='accounts.account')),
                ('love_reaction', models.ManyToManyField(blank=True, related_name='love_reaction', to='accounts.account')),
                ('sad_reaction', models.ManyToManyField(blank=True, related_name='sad_reaction', to='accounts.account')),
                ('tag_users', models.ManyToManyField(blank=True, related_name='tag_users', to='accounts.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('wow_reaction', models.ManyToManyField(blank=True, related_name='wow_reaction', to='accounts.account')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SharePost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.TextField(choices=[('shared', 'shared')], null=True)),
                ('caption', models.TextField(blank=True, max_length=1500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('angry_reaction', models.ManyToManyField(blank=True, related_name='shared_post_angry_reaction', to='accounts.account')),
                ('haha_reaction', models.ManyToManyField(blank=True, related_name='shared_post_haha_reaction', to='accounts.account')),
                ('like_reaction', models.ManyToManyField(blank=True, related_name='shared_post_like_reaction', to='accounts.account')),
                ('likes', models.ManyToManyField(blank=True, related_name='shared_post_likes', to='accounts.account')),
                ('love_reaction', models.ManyToManyField(blank=True, related_name='shared_post_love_reaction', to='accounts.account')),
                ('referer_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='posts.post')),
                ('sad_reaction', models.ManyToManyField(blank=True, related_name='shared_post_sad_reaction', to='accounts.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('wow_reaction', models.ManyToManyField(blank=True, related_name='shared_post_wow_reaction', to='accounts.account')),
            ],
        ),
    ]