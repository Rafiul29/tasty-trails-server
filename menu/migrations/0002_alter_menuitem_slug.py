# Generated by Django 4.2.14 on 2024-08-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='slug',
            field=models.SlugField(max_length=100, null=True),
        ),
    ]
