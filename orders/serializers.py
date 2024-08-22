from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from .models import DeliveryAddress,Order,OrderItem
from carts.models import CartItem
from menu.serializers import MenuItemSerializer
from account.models import User
from account.serializers import UserProfileSerializer,UserRegistrationSerializer
import uuid

class DeliveryAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model=DeliveryAddress
    fields='__all__'


class OrderItemSerializer(serializers.ModelSerializer):
  menu_item=MenuItemSerializer()
  class Meta:
    model=OrderItem
    fields='__all__'


class OrderSerializer(serializers.ModelSerializer):
  delivery_address = DeliveryAddressSerializer()
  user=UserProfileSerializer()
  class Meta:
    model=Order
    fields='__all__'

  def create(self, validated_data):
   
    delivery_address_data = validated_data.pop('delivery_address')
    user = self.context['request'].user
  
    active_cart_items = CartItem.objects.filter(user=user, is_active=True)

    if not active_cart_items.exists():
        raise ValidationError("No active cart items found for the user.")
    
    order_total = sum(item.quantity * item.menu_item.price for item in active_cart_items)

    tax=(2*order_total)/100
    order_total+=tax
    order_number=str(uuid.uuid4())[:10].replace('-', '').upper()

    # //create  delivery adderess
    delivery_address = DeliveryAddress.objects.create(**delivery_address_data)

    # create order
    order = Order.objects.create(delivery_address=delivery_address,order_number=order_number,order_total=order_total,**validated_data)

    # create order item
    for item in active_cart_items:
        OrderItem.objects.create(
                user=user,
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price
     )

    active_cart_items.delete()
    return order
  
  def update(self, instance, validated_data):
        # Only update the status field
        status = validated_data.get('status', None)
        if status is not None:
            instance.status = status
            instance.save()
        return instance



