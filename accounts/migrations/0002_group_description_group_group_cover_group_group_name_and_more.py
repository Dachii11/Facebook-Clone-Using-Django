# Generated by Django 4.1.7 on 2023-05-03 11:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='group_cover',
            field=models.ImageField(default='default_cover.png', upload_to='group_covers'),
        ),
        migrations.AddField(
            model_name='group',
            name='group_name',
            field=models.CharField(max_length=70, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='memebers',
            field=models.ManyToManyField(to='accounts.account'),
        ),
        migrations.AddField(
            model_name='group',
            name='rule_description',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='group',
            name='rule_title',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='cover_img',
            field=models.ImageField(default='default_cover.png', upload_to='backgrokund_images'),
        ),
        migrations.CreateModel(
            name='GroupPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('type', models.TextField(choices=[('groupPost', 'groupPost')], null=True)),
                ('caption', models.TextField(blank=True, max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('angry_reaction', models.ManyToManyField(blank=True, related_name='group_post_angry_reaction', to='accounts.account')),
                ('haha_reaction', models.ManyToManyField(blank=True, related_name='group_post_haha_reaction', to='accounts.account')),
                ('like_reaction', models.ManyToManyField(blank=True, related_name='group_post_like_reaction', to='accounts.account')),
                ('likes', models.ManyToManyField(blank=True, related_name='group_post_likes', to='accounts.account')),
                ('love_reaction', models.ManyToManyField(blank=True, related_name='group_post_love_reaction', to='accounts.account')),
                ('sad_reaction', models.ManyToManyField(blank=True, related_name='group_post_sad_reaction', to='accounts.account')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
                ('wow_reaction', models.ManyToManyField(blank=True, related_name='group_post_wow_reaction', to='accounts.account')),
            ],
        ),
    ]
