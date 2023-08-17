
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
     path('', SignupPage, name="signup"),
     path('login/', LoginPage, name="login"),
     path('logout/',LogoutPage,name='logout'),
     path('admins/',AdminPage,name='admins'),
     path('addjob/',Jobposting,name='addjob'),
]

