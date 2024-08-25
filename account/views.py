from django.shortcuts import render,redirect
from django.conf import settings
from rest_framework import generics
from rest_framework import viewsets,status
from rest_framework.views import APIView
from account.models import User
from .serializers import UserRegistrationSerializer,UserLoginSerializer
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
    serializer_class = UserRegistrationSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            # confirm_link=f'http://127.0.0.1:8000/api/auth/active/{uid}/{token}/'
            confirm_link=f'https://tasty-trails-server.onrender.com/api/auth/active/{uid}/{token}/'
            email_subject='Confirm Your Email for Tasty Trails'
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({'success': 'Check your confirmation mail. Please verify account!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors)   


def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode() 
        user=get_user_model().objects.get(pk=uid) 
    except get_user_model().DoesNotExist:
        user =None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # return Response({"error": "User does not have a bank account."}, status=status.HTTP_400_BAD_REQUEST)
        # return Response('User Account activate')
        return redirect(settings.LOGIN_URL)
    else:
        return Response(settings.REGISTER_URL)
    

class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data = self.request.data)
    if serializer.is_valid():
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']
      
      user = authenticate(username= username, password=password)

      if user:
         token, _ = Token.objects.get_or_create(user=user)
         login(request,user)
         return Response({'token' : token.key, 'user' :{
            "user_id":user.id,
            'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'phone_no':user.phone_no,
            'role':user.role
         }})
      else:
        return Response({'error' : "username and password incorrect"},status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors)
  

class UserLogoutView(APIView):
   
   def get(self,request):
      request.user.auth_token.delete()
      logout(request)
      return Response({"success": "User Logout Successfull"}, status=status.HTTP_200_OK)

