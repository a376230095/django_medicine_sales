"""one URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from sales import urls as app_urls
from mgr import customer
from mgr import sign_in_out
from mgr import medicine
from mgr import order
urlpatterns = [
    path('customers',customer.dispatcher),
    path('signin',sign_in_out.sign_login),
    path('signout',sign_in_out.sign_out),
    path('medicines',medicine.dispatcher),
    path('orders',order.dispatcher)
]
