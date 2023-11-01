# Generated by Django 4.1.7 on 2023-05-16 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0011_alter_comment_group_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentreply',
            name='reply_type',
            field=models.CharField(choices=[('PostCommentsReply', 'PostCommentsReply'), ('SharedPostCommentReply', 'SharedPostCommentReply'), ('GroupPostCommentReply', 'GroupPostCommentReply'), ('SharedGroupPostCommentReply', 'SharedGroupPostCommentReply')], max_length=30, null=True),
        ),
    ]