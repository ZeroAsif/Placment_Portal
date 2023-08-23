from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import JobPosting
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django. contrib import messages
from .models import JobPosting



# Create your views here.

def SignupPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and conform password are not Same!!")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
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
    try:
        job_posting = JobPosting.objects.all().order_by("-id")
        return render(request,'admin.html',{'job_posting':job_posting})
    except:
        return render(request,"admin.html")
    

def LogoutPage(request):
    logout(request)
    return redirect('login')
# ADD COMPANY HERE

def Jobposting(request):
    try:
        if request.method == 'POST':
            j_title = request.POST.get('j_title','')
            c_name = request.POST.get('c_name','')
            location = request.POST.get('j_location','')
            description = request.POST.get('j_description','')
            requirements = request.POST.get('requirments','')
            salary_range = request.POST.get('salary_range','')

            

            obj = JobPosting(job_title = j_title, company_name = c_name, location = location, description = description, requirements = requirements, salary_range = salary_range,)
            obj.save()
            messages.success(request,"Add Insruments Successfully")
            return redirect('admins')
    except:
            messages.error(request,"Please Fill Correct Information")
            return redirect('admins')



# delete button functin here
def delete_job_posting(request, job_id):
    try:
        job = JobPosting.objects.get(id=job_id)
        job.delete()
    except JobPosting.DoesNotExist:
        pass  # Handle case when job posting doesn't exist

    return redirect('admins')  # Redirect to the job list page after deletion


# def job_list_view(request):
#     job_posting = JobPosting.objects.all()  # Retrieve job postings from your model
#     context = {'job_posting': job_posting}
#     return render(request, 'your_template_name.html', context)



# update button function here


def update_job_posting(request, job_id):
    if request.method == 'POST':
        try:
            job = JobPosting.objects.get(id=job_id)
            job.job_title = request.POST.get('job_title')
            # Update other attributes similarly
            job.save()
        except JobPosting.DoesNotExist:
            pass  # Handle case when job posting doesn't exist

    return redirect('admins')  # Redirect to the job list page after update




def update_job_posting(request, job_id):
    if request.method == 'POST':
        try:
            job = JobPosting.objects.get(id=job_id)
            job.job_title = request.POST.get('job_title')
            job.company_name = request.POST.get('company_name')
            # ... update other fields

            # Update hiring status based on the checkbox value
            hiring_status = request.POST.get('hiring_status')
            job.hiring_status = 'Hiring' if hiring_status else 'hiring Closed'

            job.save()
        except JobPosting.DoesNotExist:
            pass  # Handle case when job posting doesn't exist

    return redirect('admins')










# student intrested data
# from django.shortcuts import render


# def admin_view_interested_students(request):
#     interested_students = Job_application.objects.filter(interested=True).select_related('user')
#     return render(request, 'admin_interested_students.html', {'interested_students': interested_students})