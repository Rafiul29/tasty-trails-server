from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from sslcommerz_lib import SSLCOMMERZ

class PaymentViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        # SSLCommerz configuration
        settings = {
            'store_id': 'techn671e3a7c8eda9',
            'store_pass': 'techn671e3a7c8eda9@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(settings)

        # Extract data from the request
        total_amount = request.data.get('total_amount', 100.26)
        currency = request.data.get('currency', "BDT")
        tran_id = request.data.get('tran_id', "12345")
        success_url = request.data.get('success_url', "your success url")
        fail_url = request.data.get('fail_url', "your fail url")
        cancel_url = request.data.get('cancel_url', "your cancel url")
        cus_name = request.data.get('cus_name', "test")
        cus_email = request.data.get('cus_email', "test@test.com")
        cus_phone = request.data.get('cus_phone', "01700000000")
        cus_add1 = request.data.get('cus_add1', "customer address")
        cus_city = request.data.get('cus_city', "Dhaka")
        cus_country = request.data.get('cus_country', "Bangladesh")
 
        # Create payment information
        post_body = {
            'total_amount': total_amount,
            'currency': currency,
            'tran_id': tran_id,
            'success_url': success_url,
            'fail_url': fail_url,
            'cancel_url': cancel_url,
            'emi_option': 0,
            'cus_name': cus_name,
            'cus_email': cus_email,
            'cus_phone': cus_phone,
            'cus_add1': cus_add1,
            'cus_city': cus_city,
            'cus_country': cus_country,
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': "Test",
            'product_category': "Test Category",
            'product_profile': "general"
        }

        # Create payment session with SSLCommerz
        response = sslcz.createSession(post_body)
        if response.get('status') == 'SUCCESS' and 'GatewayPageURL' in response:
            print("Yes i am listening")
            return Response({"url": response['GatewayPageURL']}, status=status.HTTP_200_OK)
        return Response({"error": "Unable to create payment session"}, status=status.HTTP_400_BAD_REQUEST)