from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    CHOICES_ROLE = (
        ('customer', 'customer'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=15, choices=CHOICES_ROLE,default='customer')
    phone_no = models.CharField(max_length=20)