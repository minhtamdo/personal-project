# Generated by Django 5.0.6 on 2024-08-24 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_wishlist_name_alter_wishlist_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wishlist',
            old_name='name',
            new_name='item',
        ),
    ]
