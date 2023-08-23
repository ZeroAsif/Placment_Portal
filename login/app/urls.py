
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
     path('', SignupPage, name="signup"),
     path('login/', LoginPage, name="login"),
     path('logout/',LogoutPage,name='logout'),
     path('admins/',AdminPage,name='admins'),
     path('addjob/',Jobposting,name='addjob'),
     path('delete/<int:job_id>/', delete_job_posting, name='delete_job'),
     path('update/<int:job_id>/', update_job_posting, name='update_job'),
     

]



