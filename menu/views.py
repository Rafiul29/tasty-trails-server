from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from django.db import IntegrityError

from .serializers import MenuItemSerializer,FavouriteSerializer
from .models import MenuItem,Favourite


# Create your views here.
class MenuItemViewSet(viewsets.ModelViewSet):
  queryset=MenuItem.objects.all()
  serializer_class=MenuItemSerializer
  filter_backends=[filters.SearchFilter]
  search_fields = ['category__name','category__slug','name','slug']

  def get_queryset(self):
      return super().get_queryset()
  

class FavouriteSpecificAdvertisement(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    print(user_id)
    if user_id:
      return query_set.filter(user=user_id)
    return query_set
# http://127.0.0.1:8000/menu/favourite/?user_id=2

class FavouriteViewSet(viewsets.ModelViewSet):
  queryset=Favourite.objects.all()
  serializer_class=FavouriteSerializer
  serializer_class=FavouriteSerializer
  filter_backends=[FavouriteSpecificAdvertisement]

  def create(self,request,*args, **kwargs):
    user =  self.request.data.get('user')
    menu_item = request.data.get('menu_item')
    
    # check if the user has already added this menu item to their favourite
    if Favourite.objects.filter(user=user,menu_item=menu_item).exists():
      return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      return super().create(request, *args, **kwargs)
    except IntegrityError:
      return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
    