"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from polls.views import *
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('api/v1/logout/',LogoutView.as_view(), name='user-logout'),
    path('api/v1/login/',LoginView.as_view(), name='user-login'),
    path('api/v1/gettoken/', TokenObtainPairView.as_view(), name='gettoken'),
    path('api/v1/countries/', CountryView.as_view(), name='country'),
    path('api/v1/sale_statistics/',SalesView.as_view(), name='salesall'),
    path('api/v1/users/<int:id>',EditUserView.as_view(), name='edituser'),
    path('api/v1/sales/',SalesUserView.as_view(), name='salesuseronly'),
    path('api/v1/sales/<int:id>',NewSalesUserView.as_view(), name='salesuser'),
    path('api/v1/import/place',UploadCountryAndCityView.as_view(), name='salesuser'),
    path('api/v1/import/sales',UploadSalesView.as_view(), name='salesuser'),
    
]
