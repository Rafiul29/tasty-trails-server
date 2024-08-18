from django.urls import path,include
from .views import UserRegistrationView,activate

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('active/<uid64>/<token>/',activate,name='active'),
]
