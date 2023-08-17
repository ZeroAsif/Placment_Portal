from django.shortcuts import render
from django.contrib.auth.decorators import  login_required
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render(request,'user_templates/home.html')


def ViewProfile(request):
    return render(request,'user_templates/viewprofile.html')