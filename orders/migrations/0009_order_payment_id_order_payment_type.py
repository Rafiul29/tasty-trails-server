# Generated by Django 4.2.14 on 2024-10-27 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_orderitem_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('Card', 'Card'), ('Cash On', 'Cash On'), ('Mobile Banking', 'Mobile Banking'), ('Account Balance', 'Account Balance')], default='Cash On', max_length=20),
        ),
    ]