# Generated by Django 5.0.6 on 2024-07-26 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_product_specifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='specifications',
        ),
    ]
