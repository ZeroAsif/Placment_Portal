from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django. contrib import messages
from .models import JobPosting
from django.core.paginator import Paginator
from Student.models import Job_application
from django.core.exceptions import ObjectDoesNotExist
from .helper import send_forget_password_mail
from .models import *
import uuid
import xlwt
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.db.models import Q



""" Send Email function defined while user register"""


User = get_user_model()
def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    verification_link = f'http://{current_site.domain}/verify_email/{uid}/{token}/'
    subject = 'Verify Your Email'
    message = message = f'Click the following link to verify your email:\n{verification_link}'
    send_mail(subject, message, 'shaikhsaud8286@gmail.com', [user.email])


def verify_email(request, uid, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Email verification successful. You can now log in.')
        else:
            messages.error(request, 'Invalid email verification link.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    except Exception as e:
        messages.error(request, 'Something went wrong during email verification.')
    return redirect('login')  # You should replace 'login' with the actual login URL


def check_email(request):

    return render(request, 'check_email_page.html')


""" Sigup Function are here """


def SignupPage(request):
    try:
        if request.method == 'POST':
            uname = request.POST.get('username')
            email = request.POST.get('email', '')
            pass1 = request.POST.get('password1')
            pass2 = request.POST.get('password2')
            if not email.endswith(('pg.ictmumbai.edu.in', 'ug.ictmumbai.edu.in')):
                messages.error(request, 'Email domain must be pg.ictmumbai.edu.in or ug.ictmumbai.edu.in')
            elif not email:
                messages.error(request, 'Email prefix is required')
            elif len(pass1) < 8:
                messages.error(request, 'Password must be at least 8 characters long')
            elif pass1 != pass2:
                messages.error(request, 'Passwords do not match')
            elif User.objects.filter(Q(email=email) | Q(username=uname)).exists():
               messages.error(request, 'Username or Email address already exists')
            else:
                #Create the user and set as inactive
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                my_user.is_active = False
                my_user.save()
                # Send email verification
                send_verification_email(my_user, request)
                messages.success(request, 'Please check your email for a verification link.')
                return redirect('check_email_page')
        return render(request, 'signup.html')
    except Exception as e:
        # Handle other exceptions here
        messages.error(request, 'Something went wrong, please try again')
    return redirect('signup')


""" Login Function are here """


# @login_required(login_url='login')
def LoginPage(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email, password=password)
            if user.is_active == False:
                messages.error(request,'Cannot Login until you recieved a Verification Mail')
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    if email.endswith(('pg.ictmumbai.edu.in', 'ug.ictmumbai.edu.in')):
                        return redirect('admins')
                    else:
                        messages.error(request, 'Superusers must use pg.ictmumbai.edu.in or ug.ictmumbai.edu.in domain')
                else:
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        return render(request, 'login.html')
    except:
        messages.error(request, 'Something went wrong please try again')
        return redirect('login')


""" Show the admin page"""


@login_required(login_url='login')
def AdminPage(request):
    try:
        job_posting = JobPosting.objects.all().order_by("-created_at")
        context = []
        s_data = []
        for job in job_posting:
            jdata = job
            sdata = Job_application.objects.filter(job_posting=job, interested=True)
            s_data.append(sdata)
            context.append({'jdata': jdata, 'sdata': sdata})

        # Pagination
        paginator = Paginator(job_posting, 5)
        page_numbers = request.GET.get('page')
        job_posting = paginator.get_page(page_numbers)


    except ObjectDoesNotExist:
        job_posting = []
        context = []

    return render(request, 'admin.html', {'job_posting': job_posting, 'sdata': s_data, 'context': context,  })


""" Logout are defined here"""
@login_required(login_url='login')
def LogoutPage(request):
    logout(request)
    messages.success(request, 'You have logout')
    return redirect('login')


""" Jobposting function are here """
@login_required(login_url='login')
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
            messages.success(request,"Company Added Successfully")
            return redirect('admins')
    except:
        messages.error(request,"Please Fill Correct Information")
        return redirect('admins')



""" delete button functin here """
@login_required(login_url='login')
def delete_job_posting(request, job_id):
    try:
        job = JobPosting.objects.get(id=job_id)
        job.delete()
    except JobPosting.DoesNotExist:
        pass  # Handle case when job posting doesn't exist

    return redirect('admins')  # Redirect to the job list page after deletion


""" JOB List views are here """
@login_required(login_url='login')
def job_list_view(request):
    job_posting = JobPosting.objects.all()  # Retrieve job postings from your model
    context = {'job_posting': job_posting}
    return render(request, 'admins.html', context)


""" update button function here """


@login_required(login_url='login')
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
            messages.success(request, "Update Successfully")
            return redirect('admins')
        except JobPosting.DoesNotExist:
            messages.error(request, "Something went wrong")
            return redirect('admins')

    return redirect('admins')  # Redirect to the job list page after update


""" Export Excel are defined are here"""
@login_required(login_url='login')
def ExportExcel(request, job_id):
    if request.method == 'POST':
        print('inside post export')
    if request.method == 'GET':
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="data_export.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Data Export')

        # Write headers
        headers = ['Sr.No', 'Name', 'Email', 'Phone Number', 'College ID']
        for col_num, header_title in enumerate(headers):
            ws.write(0, col_num, header_title)

        student_data = Job_application.objects.filter(job_posting__id=job_id ,interested=True)
        # Fetch data from your model or construct a list of dictionaries containing the data
        data = []
        for s_d in student_data:
            data .append(             
                {'Sr.No': s_d.user.personalinfo.student_id, 
                 'Name': s_d.user.personalinfo.first_name, 
                 'Email':  s_d.user.email, 
                 'Phone Number':  s_d.user.personalinfo.phone_number, 
                 'College ID':s_d.user.personalinfo.student_college_id},
            )

        # Write data rows
        for row_num, row_data in enumerate(data, start=1):
            for col_num, value in enumerate(row_data.values()):
                ws.write(row_num, col_num, value)

        wb.save(response)
        return response

""" Change password are define here """

def ChangePassword(request , token):
    context = {}
    try:
        profile_obj = reset_password.objects.filter(forgot_password_token = token).first()

        context = {'user_id' : profile_obj.user.id}
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id',)
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'change-password{token}')
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'change-password{token}')
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

    except Exception as e:
        pass
    return render(request , 'change-password.html' , context)




""" Change password are create here"""
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not User.objects.filter(email=email).first():
                messages.error(request, 'No user found with this email.')
                return redirect('forget-password')

            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            # Create the reset_password object but don't save it yet
            profile_obj, created = reset_password.objects.get_or_create(user=user_obj)
            send_forget_password_mail(user_obj.email , token)
            # Save the token to the profile_obj after sending the email
            profile_obj.forgot_password_token = token
            profile_obj.save()

            messages.success(request, 'An email is sent.')
            return redirect('forget_password')
        return render(request , 'forget-password.html')
    except:
        messages.error(request, " Something is wrong")
        return redirect('login')



def save_selected_students(request):
    selected_student_id = request.POST.get('selected_students')
    job_id = request.POST.get('job_students')

    try:
        user_obj = User.objects.get(id=selected_student_id)
        job_obj = JobPosting.objects.get(id=job_id)

        # Check if the student is already selected
        if SelectedStudent.objects.filter(user=user_obj, company_name=job_obj).exists():
            messages.success(request,"Successfully selected student")
            return render (request,'admin.html')

        # Create a new SelectedStudent object with the "You Are Selected" message
        obj = SelectedStudent.objects.create(
            user=user_obj,
            company_name=job_obj,
            selected=True,
            message="You Are Selected"
        )
        obj.save()

        return HttpResponse("You Are Selected")
    except User.DoesNotExist:
        return HttpResponse("Already selected.")
    except JobPosting.DoesNotExist:
        return HttpResponse("Job posting not found.")

