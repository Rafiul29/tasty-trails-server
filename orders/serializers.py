from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated

from .models import DeliveryAddress,Order,OrderItem


class OrderSerializer(serializers.ModelSerializer):
  class Meta:
    model=Order
    fields='__all__'


class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model=OrderItem
    fields='__all__'


class DeliveryAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model=DeliveryAddress
    fields='__all__'

