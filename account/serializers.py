from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True) 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','phone_no','role','password', 'confirm_password']

      
      
    def save(self):
      username = self.validated_data['username']
      first_name = self.validated_data['first_name']
      last_name = self.validated_data['last_name']
      email = self.validated_data['email']
      password = self.validated_data['password']
      password2 = self.validated_data['confirm_password']
      phone_no = self.validated_data['phone_no']
      role = self.validated_data['role']
      
    
      if password != password2:
        raise serializers.ValidationError({'error' : "Password don't match"})
      
      if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-+]).{8,}$', password):
        raise serializers.ValidationError({"error":"This password must contain at least 8 characters, one uppercase letter, one lowercase letter, one digit and one symbol."})
      
      if User.objects.filter(email=email).exists():
          raise serializers.ValidationError({'error' : "Email Already exists"})
      
      account = User(username = username, email=email, first_name = first_name, last_name = last_name,phone_no=phone_no,role=role)
      account.set_password(password)
      account.is_active=False
      account.save()
      return account



class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField(required = True)
  password = serializers.CharField(required = True)



