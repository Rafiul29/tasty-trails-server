from django.db import models
from account.models import User
from category.models import Category

# Create your models here.
class MenuItem(models.Model):
  name=models.CharField(max_length=200,unique=True)
  description=models.TextField()
  ingredients=models.CharField(max_length=200)
  price=models.DecimalField(max_digits=10,decimal_places=2)
  image=models.ImageField(upload_to='menu/images/')
  slug=models.SlugField(max_length=200,null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  discount=models.IntegerField(null=True,blank=True,default=0)
  avarate_rating=models.IntegerField(null=True,blank=True,default=0)
  count_reviewer=models.IntegerField(null=True,blank=True,default=0)
  rating_sum=models.IntegerField(null=True,blank=True,default=0)
  
  user=models.ForeignKey(User,related_name='menuitem',on_delete=models.CASCADE)
  category=models.ForeignKey(Category,related_name='category',on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
class Favourite(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
  created_at=models.DateTimeField(auto_now_add=True)


  def __str__(self):
    return self.menu_item.name


STAR_CHOICES=[
  ('1','⭐'),
  ('2','⭐⭐'), 
  ('3','⭐⭐⭐'),
  ('4','⭐⭐⭐⭐'),
  ('5','⭐⭐⭐⭐⭐')
]
class Review(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
  comment=models.TextField()
  rating=models.CharField(choices=STAR_CHOICES,max_length=1)
  created_at=models.DateTimeField(auto_now_add=True)







