from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ
from orders.models import Order, DeliveryAddress,OrderItem
from carts.models import CartItem
import uuid
from rest_framework import status  # Make sure this import is at the top of your file
from django.conf import settings
from django.shortcuts import redirect
from account.models import User

class PaymentViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        # SSLCommerz configuration
        sslcz_settings = {
            'store_id': 'techn671e3a7c8eda9',
            'store_pass': 'techn671e3a7c8eda9@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(sslcz_settings)
        
        # Generate unique transaction ID
        tran_id = str(uuid.uuid4())[:10].replace('-', '').upper()
        
        # Extract and set default request data
        user_id = request.data.get('user')
        total_amount = request.data.get('total_amount', 0.26)
        currency = request.data.get('currency', "BDT")
        name = request.data.get('name', "name")
        email = request.data.get('email', "test@test.com")
        phone_no = request.data.get('phone_no', "01700000000")
        address_line_1 = request.data.get('address_line_1', "customer address")
        address_line_2 = request.data.get('address_line_2', "customer address")
        city = request.data.get('city', "Dhaka")
        country = request.data.get('country', "Bangladesh")
        postal_code = request.data.get('postal_code', "14141")
        payment_type = request.data.get('payment_type', "Online Payment")
        state = request.data.get('state', "state")
        
        # Define callback URLs
        success_url = request.build_absolute_uri(f'/payment/success/?tran_id={tran_id}&user_id={user_id}&name={name}&email={email}&phone_no={phone_no}&address_line_1={address_line_1}&address_line_2={address_line_2}&city={city}&country={country}&postal_code={postal_code}&status={status}&payment_type={payment_type}&state={state}')
        fail_url = request.build_absolute_uri(f'/payment/cancle/')
        fail_url = request.build_absolute_uri('/payment/fail/')
        cancel_url = request.build_absolute_uri('/payment/cancel/')

        # Create payment information payload
        post_body = {
            'total_amount': total_amount,
            'currency': currency,
            'tran_id': tran_id,
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'emi_option': 0,
            'cus_name': name,
            'cus_email': email,
            'cus_phone': phone_no,
            'cus_add1': address_line_1,
            'cus_city': city,
            'cus_country': country,
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Test",
            'product_category': "Test Category",
            'product_profile': "general"
        }

        try:
            user=User.objects.get(id=user_id)
            active_cart_items = CartItem.objects.filter(user=user, is_active=True)
            if not active_cart_items.exists():
                return Response({"error": "No active cart items found for the user."}, status=status.HTTP_404_NOT_FOUND)
            response = sslcz.createSession(post_body)
            if response.get('status') == 'SUCCESS' and 'GatewayPageURL' in response:
                return Response({"url": response['GatewayPageURL']})
            return Response({"error": "Unable to create payment session"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def success(self, request):
        try:
            # Extract parameters
            user_id = request.query_params.get('user_id')
            tran_id = request.query_params.get('tran_id')
            name = request.query_params.get('name')
            email = request.query_params.get('email')
            phone_no = request.query_params.get('phone_no')
            address_line_1 = request.query_params.get('address_line_1')
            address_line_2 = request.query_params.get('address_line_2')
            city = request.query_params.get('city')
            country = request.query_params.get('country')
            postal_code = request.query_params.get('postal_code')
            payment_type = request.query_params.get('payment_type')
            state = request.query_params.get('state')

            # Get user and active cart items
            user = User.objects.get(id=user_id)
            active_cart_items = CartItem.objects.filter(user=user, is_active=True)
            if not active_cart_items.exists():
                return Response({"error": "No active cart items found for the user."}, status=status.HTTP_404_NOT_FOUND)

            # Calculate order totals
            order_total, total_discount = 0, 0
            for cart_item in active_cart_items:
                discount = (cart_item.menu_item.price * cart_item.menu_item.discount / 100) * cart_item.quantity
                total_discount += discount
                order_total += (cart_item.menu_item.price * cart_item.quantity) - discount
            tax = (2 * order_total) / 100
            order_total += tax

            # Create delivery address
            delivery_address = DeliveryAddress.objects.create(
                user=user, name=name, email=email, phone_no=phone_no,
                address_line_1=address_line_1, address_line_2=address_line_2,
                city=city, postal_code=postal_code, country=country,state=state
            )

            # Create order
            order_number = str(uuid.uuid4())[:10].replace('-', '').upper()
            order = Order.objects.create(
                user=user, order_number=order_number, delivery_address=delivery_address,
                payment_type=payment_type, payment_status='Success', payment_id=tran_id,
                total_discount=total_discount, order_total=order_total
            )
            # create order item
            for item in active_cart_items:
                OrderItem.objects.create(
                user=user,
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price-item.menu_item.price*item.menu_item.discount/100
                )

            active_cart_items.delete()

            return redirect(settings.SUCCESS_URL)

        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def cancel(self, request):
        return redirect(settings.CANCEL_URL)
    
    @action(detail=False, methods=['post'])
    def fail(self, request):
        return redirect(settings.FAIL_URL)
