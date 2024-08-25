
from rest_framework import serializers
from account.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name', 'email','phone_no','role']


