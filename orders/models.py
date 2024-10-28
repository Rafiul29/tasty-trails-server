from django.db import models
from account.models import User
from menu.models import MenuItem
import uuid
from django.utils.dateparse import parse_datetime

# Create your models here.
class DeliveryAddress(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  name=models.CharField(max_length=255,null=True)
  email=models.CharField(max_length=100,null=True)
  phone_no=models.CharField(max_length=20)
  address_line_1 = models.CharField(max_length=255)
  address_line_2 = models.CharField(max_length=255, blank=True, null=True)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=20)
  country = models.CharField(max_length=100)

  def __str__(self) -> str:
    return f"{self.address_line_1}, {self.city}, {self.country}"

status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

payment_type_choices = [
        ('Cash On Delivary', 'Cash On Delivary'),
        ('Online Payment', 'Online Payment'),
    ]

payment_status = [
        ('Success', 'Success'),
        ('Cancle', 'Cancle'),
        ('Failed', 'Failed'),
        ('Pending', 'Pending')
    ]


class Order(models.Model):
  order_number=models.CharField(max_length=10,unique=True,blank=True,null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, null=True,blank=True)
  order_total = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
  order_date = models.DateTimeField(auto_now_add=True)
  total_discount=models.IntegerField(null=True,blank=True,default=0)
  payment_id=models.CharField(null=True,blank=True,default=0)
  payment_type=models.CharField(max_length=20, choices=payment_type_choices, default='Cash On Delivary')
  payment_status=models.CharField(max_length=20,choices=payment_status, default='Pending')
  status = models.CharField(max_length=20, choices=status_choices, default='Pending')

  def __str__(self) -> str:
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.quantity} x {self.menu_item.name}"

