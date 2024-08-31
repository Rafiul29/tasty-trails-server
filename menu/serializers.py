from rest_framework import serializers
from .models import MenuItem, Favourite, Review
from category.serializers import CategorySerializer
from tasty_trails.serializers import UserProfileSerializer

from account.models import User

class MenuItemSerializer(serializers.ModelSerializer):
  # category=CategorySerializer()
  class Meta:
    model=MenuItem
    fields='__all__'


class FavouriteSerializer(serializers.ModelSerializer):
  # user=serializers.StringRelatedField(many=False)
  menu_item=MenuItemSerializer()
  class Meta:
    model=Favourite
    fields='__all__'
    

class ReviewSerializer(serializers.ModelSerializer):
   user = UserProfileSerializer()  

   class Meta:
    model=Review
    fields=['id', 'user', 'menu_item', 'comment', 'rating', 'created_at']
    