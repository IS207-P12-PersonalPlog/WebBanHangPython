# Generated by Django 5.1.3 on 2024-12-13 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0016_rename_user_id_cartitem_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cartitem',
        ),
    ]
