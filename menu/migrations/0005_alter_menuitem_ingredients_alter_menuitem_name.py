# Generated by Django 4.2.14 on 2024-08-20 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_menuitem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='ingredients',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
