from django.db import models
from account.models import User
from menu.models import MenuItem

# Create your models here.
class Cart(models.Model):
  cart_id=models.CharField(max_length=250,blank=True)
  date_added=models.DateField(auto_now_add=True)

  def __str__(self) -> str:
    return self.cart_id

class CartItem(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
  menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
  quantity=models.IntegerField()
  is_active=models.BooleanField(default=True)

  def __str__(self) -> str:
    return self.menu_item.name