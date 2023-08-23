
from django.urls import path
from .views import *

urlpatterns = [
    path("home",HomePage,name='home'),
    path("viewprofile",ViewProfile,name='viewprofile'),
]

