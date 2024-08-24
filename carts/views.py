from django.shortcuts import render,redirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


from .models import CartItem,Cart
from .serializers import CartItemSerializer
from menu.models import MenuItem

# Create your views here.
def _cart_id(request):
  cart=request.session.session_key
  if not cart:
    cart=request.session.create()
  return cart


class SpecificUserCartItem(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    if user_id:
      return query_set.filter(user=user_id,is_active=True)
    return query_set


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    filter_backends = [SpecificUserCartItem]
    def create(self, request, *args, **kwargs):
        user = self.request.user
        menu_item = request.data.get('menu_item')
      
        menu=MenuItem.objects.get(id=menu_item)

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        try:
          if CartItem.objects.filter(user=user,menu_item=menu_item).exists():
            cart_item=CartItem.objects.get(menu_item=menu,user=user)
            cart_item.quantity+=1
            cart_item.save()
            return Response({"success": "Cart item increase quantity"}, status=status.HTTP_200_OK)
          else:
            cart_item = CartItem.objects.create(
              menu_item=menu,
              quantity=1,
              cart=cart,
              user=user
              )
            cart_item.save()
            return Response({"success": "Item added into cart"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
          return Response({"error": "Item does not added into cart"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
      user = self.request.user
      menu_item = request.data.get('menu_item')
      quantity = request.data.get('quantity')

      menu=MenuItem.objects.get(id=menu_item)

      try:
          if CartItem.objects.filter(user=user,menu_item=menu_item).exists():
            cart_item=CartItem.objects.get(menu_item=menu,user=user)
            if int(quantity)==0:
               cart_item.delete()
               return Response({"success": "Cart item removed successfully."}, status=status.HTTP_200_OK)
            elif cart_item.quantity<int(quantity):
              cart_item.quantity+=1
              cart_item.save()
              return Response({"increase": "increase cart quantity"}, status=status.HTTP_200_OK)
            else:
              cart_item.quantity-=1
              cart_item.save()
              return Response({"decrease": "decrease cart quantity"}, status=status.HTTP_200_OK)
            
      except CartItem.DoesNotExist:
          return Response({"error": "menu item does not update into cart"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"success": "Cart item removed successfully."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def checkout(request):
    try:
      tax=0
      grand_total=0
      total=0

      cart_items= CartItem.objects.filter(user=request.user,is_active=True)
  
      for cart_item in cart_items:
         total+=cart_item.menu_item.price*cart_item.quantity
      tax=(2*total)/100
      grand_total=total+tax

      return Response({"result": {
         'total':total,
         'tax':tax,
         'grand_total':grand_total
      }}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)