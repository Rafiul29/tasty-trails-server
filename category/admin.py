from django.contrib import admin
from  .models import Category
# Register your models here.

class AdminCategory(admin.ModelAdmin):

  list_display=['id','name','slug']
  prepopulated_fields={'slug':('name',),}

admin.site.register(Category,AdminCategory)

