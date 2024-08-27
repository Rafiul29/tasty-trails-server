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



class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE )
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.account_no}"
  
    class Meta:
        verbose_name_plural = "UserBankAccount"