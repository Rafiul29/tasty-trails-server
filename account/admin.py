from django.contrib import admin
from .models import User,UserBankAccount
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  list_display=['id','username','first_name','last_name','email','phone_no','role']

admin.site.register(User,UserAdmin)


class UserBankAccoutAdmin(admin.ModelAdmin):
  list_display=['id','account_no','balance']

admin.site.register(UserBankAccount,UserBankAccoutAdmin)