# Generated by Django 4.1.7 on 2023-05-06 16:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_grouppost_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouppost',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='grouppost',
            name='file',
            field=models.FileField(blank=True, upload_to='GroupPostsIcons'),
        ),
        migrations.AddField(
            model_name='grouppost',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='group_views', to='accounts.account'),
        ),
        migrations.AlterField(
            model_name='grouppost',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='GroupSharePost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.TextField(choices=[('groupShared', 'groupShared')], null=True)),
                ('caption', models.TextField(blank=True, max_length=1500)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('angry_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_angry_reaction', to='accounts.account')),
                ('haha_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_haha_reaction', to='accounts.account')),
                ('like_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_like_reaction', to='accounts.account')),
                ('likes', models.ManyToManyField(blank=True, related_name='group_shared_post_likes', to='accounts.account')),
                ('love_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_love_reaction', to='accounts.account')),
                ('referer_post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_shares', to='accounts.grouppost')),
                ('sad_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_sad_reaction', to='accounts.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('views', models.ManyToManyField(blank=True, related_name='groupSharePostView', to='accounts.account')),
                ('wow_reaction', models.ManyToManyField(blank=True, related_name='group_shared_post_wow_reaction', to='accounts.account')),
            ],
        ),
    ]
