# Generated by Django 4.2.14 on 2024-08-20 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_alter_menuitem_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
    ]