# Generated by Django 5.1.3 on 2024-11-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='brands',
            fields=[
                ('brand_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('brand_title', models.CharField(max_length=100)),
            ],
        ),
    ]
