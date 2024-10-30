from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .models import DeliveryAddress,Order,OrderItem
from account.models import UserBankAccount
from carts.models import CartItem
from menu.serializers import MenuItemSerializer
from account.models import User
from account.serializers import UserRegistrationSerializer
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


# class OrderSerializer(serializers.ModelSerializer):
#   delivery_address = DeliveryAddressSerializer(required=False)
#   class Meta:
#     model=Order
#     fields='__all__'

  # def create(self, validated_data):
   
  #   delivery_address_data = validated_data.pop('delivery_address')
  #   user = self.context['request'].user
  
  #   active_cart_items = CartItem.objects.filter(user=user, is_active=True)

  #   if not active_cart_items.exists():
  #       raise ValidationError("No active cart items found for the user.")
    
  #   order_total = sum(item.quantity * item.menu_item.price for item in active_cart_items)

  #   tax=(2*order_total)/100
  #   order_total+=tax
  #   order_number=str(uuid.uuid4())[:10].replace('-', '').upper()

  #   user_account = UserBankAccount.objects.filter(user=user).first()
 
  #   if user_account is None:
  #       return ValidationError({'error' : "User does not have a bank account"})
        
  #   if int(user_account.balance) < int(order_total):
  #       print("yes")
  #       return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
  #       return ValidationError({'error' : "User does not have a bank account"})

  #   print('done')


  #   #create  delivery adderess
  #   delivery_address = DeliveryAddress.objects.create(**delivery_address_data)

  #   # create order
  #   order = Order.objects.create(delivery_address=delivery_address,order_number=order_number,order_total=order_total,**validated_data)
  #   print("order",order)
  #   # create order item
  #   for item in active_cart_items:
  #       OrderItem.objects.create(
  #               user=user,
  #               order=order,
  #               menu_item=item.menu_item,
  #               quantity=item.quantity,
  #               price=item.menu_item.price
  #    )

  #   active_cart_items.delete()
  #   return order
  

class OrderSerializer(serializers.ModelSerializer):
    delivery_address = DeliveryAddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
      
        delivery_address_data = validated_data.pop('delivery_address')
        status = validated_data.pop('status')
        payment_type=validated_data.pop("payment_type")
        payment_status=validated_data.pop("payment_status")
        
        
     
        user = self.context['request'].user
        
        
        active_cart_items = CartItem.objects.filter(user=user, is_active=True)
        if not active_cart_items.exists():
            raise serializers.ValidationError("No active cart items found for the user.")
        
     
        # order_total = sum(item.quantity * item.menu_item.price for item in active_cart_items)
        # tax = (2 * order_total) / 100
        # order_total += tax

        order_total=0
        discount=0
        total_discount=0

        for cart_item in active_cart_items:
            discount=(cart_item.menu_item.price*cart_item.menu_item.discount/100)*cart_item.quantity
            order_total+=(cart_item.menu_item.price*cart_item.quantity)-discount
            total_discount+=discount

        tax = (2 * order_total) / 100
        order_total += tax
        
        order_number = str(uuid.uuid4())[:10].replace('-', '').upper()
        payment_id = str(uuid.uuid4())[:10].replace('-', '').upper()
     
        # user_account = UserBankAccount.objects.filter(user=user).first()

        # if user_account is None:
        #     raise serializers.ValidationError({'error': "User does not have a bank account"})

        # if user_account.balance < order_total:
        #     raise serializers.ValidationError({'error': "Insufficient balance ! Please doposit balance"})

       
        delivery_address = DeliveryAddress.objects.create(**delivery_address_data)

        order = Order.objects.create(
           delivery_address=delivery_address,order_number=order_number,payment_type=payment_type,payment_status=payment_status,payment_id=payment_id,total_discount=total_discount,order_total=order_total,**validated_data
        )
        
        for item in active_cart_items:
            OrderItem.objects.create(
            user=user,
            order=order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            price=item.menu_item.price-item.menu_item.price*item.menu_item.discount/100
            )

        # user_account.balance-=order_total
        # user_account.save()

        active_cart_items.delete()

        return order