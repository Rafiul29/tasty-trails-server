from django.shortcuts import render,redirect
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,filters,status
from django.db import IntegrityError

from .models import CartItem,Cart
from .serializers import CartItemSerializer
from menu.models import MenuItem

# Create your views here.
def _cart_id(request):
  cart=request.session.session_key
  if not cart:
    cart=request.session.create()
  return cart

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

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
            return Response({"success": "Already added into cart increase quantity"}, status=status.HTTP_200_OK)
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
            if cart_item.quantity<int(quantity):
              cart_item.quantity+=1
              cart_item.save()
              return Response({"increase": "increase cart quantity"}, status=status.HTTP_200_OK)
            else:
              cart_item.quantity-=1
              cart_item.save()
              return Response({"decrease": "decrease cart quantity"}, status=status.HTTP_200_OK)
            
      except CartItem.DoesNotExist:
          return Response({"error": "menu item does not update into cart"}, status=status.HTTP_400_BAD_REQUEST)
