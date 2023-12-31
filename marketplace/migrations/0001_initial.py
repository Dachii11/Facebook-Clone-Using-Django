# Generated by Django 4.2.2 on 2023-08-24 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, null=True)),
                ('category', models.CharField(choices=[('Apperal & Accessories', 'Apperal & Accessories'), ('Arts & Entertainment', 'Arts & Entertainment'), ('Food & Beverages', 'Food & Beverages'), ('Furniture & Hardware', 'Furniture & Hardware'), ('Business & Industrial Products', 'Business & Industrial Products'), ("Camera & equipment's", "Camera & equipment's"), ('Home & Garden', 'Home & Garden'), ('Luggage & Bags', 'Luggage & Bags'), ('Toys and Games', 'Toys and Games'), ('Vehicles & Spare Parts', 'Vehicles & Spare Parts'), ('Software', 'Software'), ('Sporting goods', 'Sporting goods'), ('Baby Products', 'Baby Products'), ('Electronics', 'Electronics'), ('Health & Beauty Products', 'Health & Beauty Products'), ('Office Supplies', 'Office Supplies')], max_length=40, null=True)),
                ('price', models.PositiveIntegerField(default=0, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
