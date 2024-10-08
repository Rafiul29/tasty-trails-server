# Generated by Django 4.2.14 on 2024-08-27 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.IntegerField(unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'UserBankAccount',
            },
        ),
    ]
