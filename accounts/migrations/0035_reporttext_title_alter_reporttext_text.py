# Generated by Django 4.2.1 on 2023-08-13 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_reporttitle_reporttext'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporttext',
            name='title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='report_text', to='accounts.reporttitle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reporttext',
            name='text',
            field=models.TextField(),
        ),
    ]