from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.views import View
from Student.views import job_application
from .models import JobPosting
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django. contrib import messages
from .models import JobPosting
from  Student.models import Job_application
import xlwt
from Student.models import *
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request,"passwords do not match")
            return redirect("signup")
        if uname and email and pass1:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        else:
            messages.error(request,'please enter all required fields')
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
            messages.error(request,"passwords or username is Wrong ")
    return render (request,'login.html')




def AdminPage(request):

        try:
            job_posting = JobPosting.objects.all().order_by("-created_at")
            context = []
            for job in job_posting:
                jdata = job
                sdata = Job_application.objects.filter(job_posting= job,interested=True)
                context.append({'jdata':jdata,'sdata':sdata})
        except ObjectDoesNotExist:
            job_posting=[]
            context=[]
        return render(request,'admin.html',{'job_posting':job_posting, 'student_data':sdata,'context':context})
       

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
            pdf_file = request.FILES.get('pdf_file')

            

            obj = JobPosting(job_title = j_title, company_name = c_name, location = location, description = description, requirements = requirements, salary_range = salary_range,pdf_file=pdf_file)
            obj.save()
            messages.success(request,"Company Added Successfully    ")
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


def job_list_view(request):
    job_posting = JobPosting.objects.all()  # Retrieve job postings from your model
    context = {'job_posting': job_posting}
    return render(request, 'admins.html', context)



# update button function here
def update_job_posting(request, job_id):
    if request.method == 'POST':
        try:
            job = JobPosting.objects.get(id=job_id)
            job.job_title = request.POST.get('job_title')
            job.company_name = request.POST.get('company_name')
            job.location = request.POST.get('location')
            job.salary_range = request.POST.get('salary_range')
            job.pdf_file = request.FILES.get('pdf_file')
            
            # ... update other fields

            # hiring status based on the checkbox value
            hiring_status = request.POST.get('hiring_status')
            job.hiring_status = hiring_status


            job.save()
        except JobPosting.DoesNotExist:
            pass  # Handle case when job posting doesn't exist

    return redirect('admins')  # Redirect to the job list page after update









# pdf post











# table to excel format 

class ExportExcelView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="data_export.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Data Export')

        # Write headers
        headers = ['#', 'Name', 'Email', 'Phone Number', 'Resume', 'Country']
        for col_num, header_title in enumerate(headers):
            ws.write(0, col_num, header_title)

        # Fetch data from your model or construct a list of dictionaries containing the data
        data = [
            {'#': '1', 'Name': 'Asif Khan', 'Email': 'pasif@gmail.com', 'Phone Number': 'Portland', 'Resume': '97219', 'Country': 'USA'},
            # Add other rows here
        ]

        # Write data rows
        for row_num, row_data in enumerate(data, start=1):
            for col_num, value in enumerate(row_data.values()):
                ws.write(row_num, col_num, value)

        wb.save(response)
        return response
