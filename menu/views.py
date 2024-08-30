from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action

from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import MenuItemSerializer,FavouriteSerializer,ReviewSerializer
from .models import MenuItem,Favourite,Review
from orders.models import Order,OrderItem

# Create your views here.
class MenuItemViewSet(viewsets.ModelViewSet):
  queryset=MenuItem.objects.all()
  serializer_class=MenuItemSerializer
  filter_backends=[filters.SearchFilter,filters.OrderingFilter]
  search_fields = ['category__slug','name','slug']
  ordering_fields = ['created_at']
  ordering = ['-created_at']

  def get_queryset(self):
      return super().get_queryset()
  
  @action(detail=False, methods=['get'])
  def discounted(self, request):
        discounted_items = MenuItem.objects.filter(discount__gt=0).order_by('-discount','-created_at')

        page = self.paginate_queryset(discounted_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(discounted_items, many=True)
        return Response(serializer.data)
  
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
    filter_backends = [SpecificFavouriteMenu,filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        menu_item = request.query_params.get('menu_item')
        queryset = self.get_queryset().order_by('-created_at')
        
        if menu_item:
            queryset = queryset.filter(menu_item=menu_item)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user  
        menu_item = request.data.get('menu_item')
        comment=request.data.get('comment'),
        rating=request.data.get('rating')

        menu= MenuItem.objects.get(id=menu_item)
        

        # Check if the user has ordered the item and the order has been delivered
        if OrderItem.objects.filter(user=user, menu_item=menu_item, order__status="Delivered").exists():
            # Check if the user has already reviewed the menu item
            # if Review.objects.filter(user=user, menu_item=menu_item).exists():
            #     return Response({"error": "You have already reviewed this menu item."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Manually create the review instance, passing the actual User instance
                review = Review.objects.create(
                    user=user,  # Pass the User instance directly
                    menu_item_id=menu_item,  # Use the menu_item ID directly
                    comment=comment,
                    rating=rating
                )
                
                # Serialize the newly created review
                serializer = ReviewSerializer(review)

                # update menu item rating sum and reviewer count
                menu.rating_sum+=int(rating)
                menu.count_reviewer+=1
                menu.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            except IntegrityError:
                return Response({"error": "An error occurred while processing your review."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You can only review menu items after your order has been delivered."}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None, *args, **kwargs):
        review = self.get_object()
        print(review.id)
        serializer = self.get_serializer(review)
        return Response(serializer.data)