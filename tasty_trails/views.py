from account.models import User
from rest_framework import viewsets,status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]
