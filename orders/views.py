from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import CartItem 
from .models import Order,OrderItem,DeliveryAddress
from .serializers import OrderSerializer,OrderItemSerializer,DeliveryAddressSerializer
import uuid

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
  queryset=Order.objects.all()
  serializer_class=OrderSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
        user = self.request.user
        delivery_address = serializer.validated_data['delivery_address']
       
        active_cart_items = CartItem.objects.filter(user=user, is_active=True)
        order_total = sum(item.quantity * item.menu_item.price for item in active_cart_items)

        tax=(2*order_total)/100
        order_total+=tax
        
        order_number=str(uuid.uuid4())[:10].replace('-', '').upper()

        # Save the order with the calculated order total
        order = serializer.save(user=user, order_total=order_total,delivery_address=delivery_address,order_number=order_number)

        for item in active_cart_items:
            OrderItem.objects.create(
                user=user,
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price
            )

        active_cart_items.delete()

class OrderItemViewSet(viewsets.ModelViewSet):
  queryset=OrderItem.objects.all()
  serializer_class=OrderItemSerializer
  permission_classes = [IsAuthenticated]

class DeliveryAddressViewSet(viewsets.ModelViewSet):
  queryset=DeliveryAddress.objects.all()
  serializer_class=DeliveryAddressSerializer