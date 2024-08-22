from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carts.models import CartItem 
from .models import Order,OrderItem,DeliveryAddress
from .serializers import OrderSerializer,OrderItemSerializer,DeliveryAddressSerializer
from rest_framework import viewsets,filters,status


class SpecificOrderUser(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    if user_id:
      return query_set.filter(user=user_id)
    return query_set


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SpecificOrderUser]

    def get_queryset(self):
        return Order.objects.filter()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class OrderItemViewSet(viewsets.ModelViewSet):
  queryset=OrderItem.objects.all()
  serializer_class=OrderItemSerializer
  permission_classes = [IsAuthenticated]


class DeliveryAddressViewSet(viewsets.ModelViewSet):
  queryset=DeliveryAddress.objects.all()
  serializer_class=DeliveryAddressSerializer