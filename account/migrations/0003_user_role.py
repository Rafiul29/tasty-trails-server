# Generated by Django 4.2.14 on 2024-08-18 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_phone_number_user_phone_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'customer'), ('admin', 'admin')], default='customer', max_length=15),
        ),
    ]
