from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from rest_framework.decorators import action

from django.db import IntegrityError
from django.db.models import Count
from .serializers import MenuItemSerializer,FavouriteSerializer,ReviewSerializer
from .models import MenuItem,Favourite,Review
from orders.models import Order,OrderItem
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum page size

class CustomPaginationMostFavourite(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100  # Maximum page size

# Create your views here.
class MenuItemViewSet(viewsets.ModelViewSet):
  queryset=MenuItem.objects.all()
  serializer_class=MenuItemSerializer
  filter_backends=[filters.SearchFilter,filters.OrderingFilter]
  search_fields = ['category__slug','name','slug']
  ordering_fields = ['created_at']
  ordering = ['-created_at']
  pagination_class = CustomPagination


  def get_queryset(self):
      return super().get_queryset()

  def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Apply search and ordering
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
  
  @action(detail=False, methods=['get'])
  def discounted(self, request):
        discounted_items = MenuItem.objects.filter(discount__gt=0).order_by('-discount','-created_at')

        page = self.paginate_queryset(discounted_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

         # Apply pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(discounted_items, request, view=self)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
  
  
  def post(self, request, *args, **kwargs):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavouriteViewSet(viewsets.ModelViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def most_favourite(self, request):

        queryset = self.get_queryset()
        queryset = queryset.values('menu_item').annotate(count=Count('menu_item')).order_by('-count')
        unique_items = [item['menu_item'] for item in queryset]
        # print(unique_items)
        
        unique_items_queryset = self.get_queryset().filter(menu_item__in=unique_items)
    
        # Use a dictionary t
        # o filter unique items by 'menu_item'
        seen = set()
        unique_items = []
        for item in unique_items_queryset:
          if item.menu_item not in seen:
             unique_items.append(item)
             seen.add(item.menu_item)

        # Apply pagination
        paginator = CustomPaginationMostFavourite()
        result_page = paginator.paginate_queryset(unique_items, request, view=self)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # user favourite menu
    @action(detail=False, methods=['get'])
    def user_favourite(self, request):
        user=request.user
        queryset = self.get_queryset()
        favouritemenus = self.queryset.filter(user=user).order_by('-created_at')

        # Apply pagination
        paginator = CustomPaginationMostFavourite()
        result_page = paginator.paginate_queryset(favouritemenus, request, view=self)
        serializer = self.get_serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # create favourite menu 
    def create(self, request, *args, **kwargs):
        user = request.user
        menu_item = request.data.get('menu_item')
        menu= MenuItem.objects.get(id=menu_item)
        # Check if the user has already added this menu item to their favourite
        if Favourite.objects.filter(user=user, menu_item=menu_item).exists():
            return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            favouritemenu=Favourite.objects.create(
                user=user,
                menu_item=menu,
            )
            serializer = FavouriteSerializer(favouritemenu)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "This item is already in your favourites."}, status=status.HTTP_400_BAD_REQUEST)
        
    # delete favourite menu item
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