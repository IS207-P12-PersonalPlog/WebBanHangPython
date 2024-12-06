# Generated by Django 5.1.3 on 2024-12-06 08:39

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0004_alter_sp_hinhanh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoadon',
            name='nghd',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
