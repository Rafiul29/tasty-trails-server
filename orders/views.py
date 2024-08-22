from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import CartItem 
from .models import Order,OrderItem,DeliveryAddress
from .serializers import OrderSerializer,OrderItemSerializer,DeliveryAddressSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
  queryset=OrderItem.objects.all()
  serializer_class=OrderItemSerializer
  permission_classes = [IsAuthenticated]

class DeliveryAddressViewSet(viewsets.ModelViewSet):
  queryset=DeliveryAddress.objects.all()
  serializer_class=DeliveryAddressSerializer