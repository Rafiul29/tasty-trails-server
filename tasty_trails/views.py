from account.models import User,UserBankAccount
from orders.models import Order
from menu.models import MenuItem
from rest_framework import viewsets,status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]


class UserBankAccountViewSet(viewsets.ModelViewSet):
    queryset = UserBankAccount.objects.all()
    serializer_class =serializers.UserBankAccountSerializer

    def get_queryset(self):
        queryset = UserBankAccount.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
           return queryset.filter(user=user_id)
        return queryset

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        balance = request.data.get('balance')
       
        if balance is None:
            return Response({"error": "balance is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            balance = int(balance)
        except ValueError:
            return Response({"error": "Invalid balance format"}, status=status.HTTP_400_BAD_REQUEST)

        if balance <= 0:
            return Response({"error": "Deposit balance must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

       
        try:
            account = UserBankAccount.objects.get(user=request.user)
        except UserBankAccount.DoesNotExist:
            return Response({"error": "User Bank Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

       
        account.balance += balance
        account.save()

        return Response({"message": "Deposit successful", "new_balance": account.balance}, status=status.HTTP_200_OK)
    


@api_view(['GET']) 
def ourstatistics(request):
    try:
      total_users=0
      total_menus=0
      complete_orders=0
      total_sales=0
      
      total_users=User.objects.all().count()
      total_menus=MenuItem.objects.all().count()
      order_delivary=Order.objects.filter(status='Delivered')
      complete_orders=order_delivary.count()

      for order in order_delivary:
          total_sales+=order.order_total

      return Response({"result": {
         'total_users':total_users,
         'total_menus':total_menus,
         'complete_orders':complete_orders,
         'total_sales':total_sales
      }}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)