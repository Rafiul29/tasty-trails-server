from rest_framework import serializers
from .models import MenuItem,Favourite
from category.serializers import CategorySerializer

class MenuItemSerializer(serializers.ModelSerializer):
  # category=CategorySerializer()
  class Meta:
    model=MenuItem
    fields='__all__'


class FavouriteSerializer(serializers.ModelSerializer):
  # user=serializers.StringRelatedField(many=False)
  # menu_item=serializers.StringRelatedField(many=False)
  class Meta:
    model=Favourite
    fields='__all__'
    