# Generated by Django 4.2.14 on 2024-08-24 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_alter_menuitem_ingredients_alter_menuitem_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(upload_to='menu/images/'),
        ),
    ]