from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from carts.models import CartItem 
from .models import Order,OrderItem,DeliveryAddress
from account.models import UserBankAccount
from .serializers import OrderSerializer,OrderItemSerializer,DeliveryAddressSerializer
from rest_framework import viewsets,filters,status
import uuid


class SpecificOrderUser(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    user_id=request.query_params.get('user_id')
    if user_id:
      return query_set.filter(user=user_id)
    return query_set.order_by('-order_date')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SpecificOrderUser]


    def get_queryset(self):
        return Order.objects.filter()


    def update(self, request, *args, **kwargs):
      print(kwargs,args)
      partial = kwargs.pop('partial', False)
      instance = self.get_object()   

      status_value = request.data.get('status')

      if status_value is not None:
          instance.status = status_value

      serializer = self.get_serializer(instance, data=request.data, partial=partial)

      if serializer.is_valid():
          self.perform_update(serializer)
          return Response(serializer.data)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SpecificOrderItemUser(filters.BaseFilterBackend):
   def filter_queryset(self,request,query_set,view):
    order_id=request.query_params.get('order_id')
    if order_id:
      return query_set.filter(order=order_id)
    return query_set


class OrderItemViewSet(viewsets.ModelViewSet):
  queryset=OrderItem.objects.all()
  serializer_class=OrderItemSerializer
  permission_classes = [IsAuthenticated]
  filter_backends = [SpecificOrderItemUser,filters.OrderingFilter]
  ordering_fields = ['created_at']
  ordering = ['-created_at']

  



class DeliveryAddressViewSet(viewsets.ModelViewSet):
  queryset=DeliveryAddress.objects.all()
  serializer_class=DeliveryAddressSerializer





