
from rest_framework import serializers
from account.models import User,UserBankAccount

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name', 'email','phone_no','role']


class UserBankAccountSerializer(serializers.ModelSerializer):
   class Meta:
    model=UserBankAccount
    fields='__all__'

