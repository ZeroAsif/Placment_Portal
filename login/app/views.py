from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import JobPosting
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django. contrib import messages



# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        print(username)
        pass1=request.POST.get('password')
        user=authenticate(request,username=username,password=pass1)
        if user is not None and user.is_staff == False:
            login(request,user)
            return redirect('home')
        
        elif user is not None and user.is_staff == True:
            login(request, user)
            return redirect('admins')
        
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def AdminPage(request):
    return render(request,"admin.html")

def LogoutPage(request):
    logout(request)
    return redirect('login')

# ADD COMPANY HERE

def Jobposting(request):
    print('>>>>>>>>>>',"enter")
    try:
        if request.method == 'POST':
            print('****************post')
            j_title = request.POST.get('j_title','')
            print('****************',j_title)
            c_name = request.POST.get('c_name','')
            print('****************',c_name)
            location = request.POST.get('j_location','')
            print('****************',location)
            description = request.POST.get('j_description','')
            print('****************',description)
            requirements = request.POST.get('requirments','')
            print('****************',requirements)
            application_deadline = request.POST.get('a_deadline','')
            print('######',application_deadline)
            
            obj = JobPosting(job_title = j_title, company_name = c_name, location = location, description = description, requirements = requirements, application_deadline = application_deadline )
            obj.save()
            messages.success(request,"Add Insruments Successfully")
            return redirect('admins')
    except:
        messages.error(request,"Please Fill Correct Information")
        return redirect('admins')