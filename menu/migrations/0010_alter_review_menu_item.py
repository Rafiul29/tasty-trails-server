# Generated by Django 4.2.14 on 2024-08-29 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0009_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='menu_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_reviews', to='menu.menuitem'),
        ),
    ]