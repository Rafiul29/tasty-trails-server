from django.contrib import admin
from .models import MenuItem, Favourite, Review
# Register your models here.

class  MenuItemAdmin(admin.ModelAdmin):
  list_display=['id','menu_name','price','category','discount','avarate_rating','user']
  prepopulated_fields={'slug':('name',),}
  def menu_name(self,obj):
    return f"{obj.name}"
   
admin.site.register(MenuItem,MenuItemAdmin)

class  FavouriteAdmin(admin.ModelAdmin):
  list_display=['id','person_name','menu_name']

  def person_name(self,obj):
    return f"{obj.user.first_name} {obj.user.last_name}"
  
  def menu_name(self,obj):
    return f"{obj.menu_item.name}"
  

admin.site.register(Favourite,FavouriteAdmin)


class  ReviewAdmin(admin.ModelAdmin):
  list_display=['id','person_name','menu_name','comment','created_at']

  def person_name(self,obj):
    return f"{obj.user.first_name} {obj.user.last_name}"
  
  def menu_name(self,obj):
    return f"{obj.menu_item.name}"
  

admin.site.register(Review,ReviewAdmin)
