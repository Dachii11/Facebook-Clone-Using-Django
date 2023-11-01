# Generated by Django 4.2.2 on 2023-09-22 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_rename_date_feelings_created_at'),
        ('comments', '0014_commentreply_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='feeling_post',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feeling_post', to='mainApp.feelings'),
        ),
    ]