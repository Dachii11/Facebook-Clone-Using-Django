# Generated by Django 4.2.2 on 2023-09-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_alter_feelings_post_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feelings',
            name='post_type',
            field=models.CharField(choices=[('feeling_post', 'feeling_post')], default='feeling_post', max_length=15, null=True),
        ),
    ]