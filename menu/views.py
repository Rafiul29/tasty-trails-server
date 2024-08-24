from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import MenuItemSerializer,FavouriteSerializer
from .models import MenuItem,Favourite

# Create your views here.
class MenuItemViewSet(viewsets.ModelViewSet):
  queryset=MenuItem.objects.all()
  serializer_class=MenuItemSerializer
  filter_backends=[filters.SearchFilter]
  search_fields = ['category__slug','name','slug']
#   parser_classes = [FormParser]

  def get_queryset(self):
      return super().get_queryset()
  
  def post(self, request, *args, **kwargs):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  

class SpecificFavouriteMenu(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    if user_id:
      return query_set.filter(user=user_id)
    return query_set


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    filter_backends = [SpecificFavouriteMenu]

    def create(self, request, *args, **kwargs):
        user = request.data.get('user')
        menu_item = request.data.get('menu_item')
        
        # Check if the user has already added this menu item to their favourite
        if Favourite.objects.filter(user=user, menu_item=menu_item).exists():
            return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"success": "Favourite removed successfully."}, status=status.HTTP_200_OK)
        except Favourite.DoesNotExist:
            return Response({"error": "Favourite not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
