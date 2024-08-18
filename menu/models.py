from django.db import models
from account.models import User
from category.models import Category

# Create your models here.
class MenuItem(models.Model):
  name=models.CharField(max_length=100,unique=True)
  description=models.TextField()
  ingredients=models.CharField(max_length=100)
  price=models.DecimalField(max_digits=10,decimal_places=2)
  image=models.ImageField(upload_to='menu/images')

  slug=models.SlugField(max_length=100,null=True,)
  user=models.ForeignKey(User,related_name='menuitem',on_delete=models.CASCADE)
  category=models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
class Favourite(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)

  def __str__(self):
    return self.menu_item.name






