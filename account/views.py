from django.shortcuts import render,redirect
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from account.models import User
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
#for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token

# Create your views here.
class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link=f'http://127.0.0.1:8000/api/auth/active/{uid}/{token}/'
            email_subject='Confirm Your Email for Tasty Trails'
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response(f'Check your mail confirmation your account number')
        
        return Response(serializer.errors)   

