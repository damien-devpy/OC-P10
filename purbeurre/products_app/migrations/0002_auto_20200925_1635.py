# Generated by Django 3.1.1 on 2020-09-25 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pict_url',
            new_name='pict_product',
        ),
    ]
