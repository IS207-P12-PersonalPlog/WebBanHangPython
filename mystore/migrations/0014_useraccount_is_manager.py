# Generated by Django 5.1.3 on 2024-12-11 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0013_remove_useraccount_allow_edit_useraccount_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]