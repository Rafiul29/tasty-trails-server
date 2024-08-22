from django.db import models
from account.models import User
from menu.models import MenuItem

# Create your models here.
class ShippingAddress(models.Model):
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
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

class Order(models.Model):
  order_number=models.CharField(max_length=10,unique=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
  order_total = models.DecimalField(max_digits=10, decimal_places=2)
  order_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, choices=status_choices, default='Pending')

  def __str__(self) -> str:
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
  order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
  quantity = models.IntegerField()
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self) -> str:
    return f"{self.quantity} x {self.menu_item.name}"

