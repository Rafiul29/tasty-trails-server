"""
URL configuration for tasty_trails project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from .views import UserProfileViewSet,UserBankAccountViewSet,ourstatistics

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('users', UserProfileViewSet)
router.register('user-bank-accounts', UserBankAccountViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/auth/',include('account.urls')),
    path('menu/',include('menu.urls')),
    path('category/',include('category.urls')),
    path('carts/',include('carts.urls')),
    path('orders/',include('orders.urls')),
    path('ourstatistics/',ourstatistics,name='ourstatistics'),
    path('', include('payment.urls')),
]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
