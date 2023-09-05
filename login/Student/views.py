import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import JobPosting
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.db import IntegrityError
from django.contrib.auth.models import User
# from xhtml2pdf import pisa
from django.template.loader import render_to_string
import uuid
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate



# Create your views here.


def Check_User_Email(request):
    try:
        if request.method == 'GET':
            email = request.GET['email_id']
            if email:
                check_email = PersonalInfo.objects.filter(email=email)
                if len(check_email) == 1:
                    return HttpResponse("Exists")
                else:
                    return HttpResponse("Not Exists")
    except:
        messages.error(request, 'Something went wrong')

def Check_Student_ID(request):
    if request.method == 'GET':
        std_id = request.GET['student_college_id']
        if std_id:
            check_std_id = PersonalInfo.objects.filter(student_college_id=std_id)
            if len(check_std_id) == 1:
                return HttpResponse("Exists")
            else:
                return HttpResponse("Not Exists")


def Check_Phone(request):
    if request.method == 'GET':
        phone = request.GET['phone']
        if phone:
            check_phone = PersonalInfo.objects.filter(phone_number=phone)
            if len(check_phone) == 1:
                return HttpResponse("Exists")
            else:
                return HttpResponse("Not Exists")


# User Home_page
@login_required(login_url='login')
def HomePage(request):
    try:
        show_job = JobPosting.objects.all().order_by("-id")
        try:
            profile_image = PersonalInfo.objects.get(student_id=request.user.id)
        except PersonalInfo.DoesNotExist:
            profile_image = None
        applied_jobs = Job_application.objects.filter(user=request.user)
        applied_jobs_ids = [job.job_posting_id for job in applied_jobs]
        context = {
            'show_job': show_job,
            'profile_image': profile_image,
            'applied_jobs_ids': applied_jobs_ids,
        }
        return render(request, 'user_templates/home.html', context)
    except:
        return render(request, 'user_templates/home.html')


# User View_Profile Page
@login_required(login_url='login')
def ViewProfile(request):
    try:
        user = request.user.id
        personal_info = PersonalInfo.objects.filter(student__id=user)
        cv = Resume.objects.filter(user__id=user)
        experience = Experience.objects.filter(user__id=user).order_by("-id")
        education = Education.objects.filter(user__id=user).order_by("-id")
        certification = Certificate.objects.filter(user__id=user).order_by("-id")
        project = Project.objects.filter(user__id=user).order_by("-id")
        additional_skill = AdditionalSkill.objects.filter(user__id=user).order_by("-id")
        context = {
            'personal_infos': personal_info,
            'cvs': cv,
            'experience': experience,
            'education': education,
            'certification': certification,
            'project': project,
            'additional_skill': additional_skill
        }
        return render(request, 'user_templates/viewprofile.html', context)
    except:
        return render(request, 'user_templates/viewprofile.html')


# def filter_jobs(request):
#     if request.method == 'GET':
#         company_name = request.GET.get('company-name')
#         employment_type = request.GET.get('employment-type')
#
#         job_data = JobPosting.objects.all()
#
#         if company_name:
#             filtered_data = job_data.filter()
#         if employment_type:
#             filtered_data = job_data.filter(name=name)


"""Student show Interest View Here."""
def job_application(request, job_id):
    try:
        job_posting = JobPosting.objects.get(id=job_id)

        # Check if an application for this job by the user already exists
        existing_application = Job_application.objects.filter(user=request.user, job_posting=job_posting).first()
        if existing_application:
            existing_application.interested = True
            existing_application.save()
        else:
            new_application = Job_application(user=request.user, job_posting=job_posting, interested=True)
            messages.success(request, 'Applied Successfully')
            new_application.save()
        return redirect('home')
    except Exception as e:
        # Handle exceptions here, e.g., log the error or provide an error message
        messages.error(request, 'Something went wrong')
        return redirect('home')


# Job Description Views Here.
def Job_Description(request, id):
    try:
        job_description = JobPosting.objects.get(id=id)
        applied_jobs = Job_application.objects.filter(user=request.user)
        applied_jobs_ids = [job.job_posting_id for job in applied_jobs]
        context = {
            "job_description": job_description,
            "applied_jobs_ids": applied_jobs_ids
        }
        return render(request, "user_templates/job_description.html", context)
    except Exception as e:
        # Handle other exceptions here, e.g., log the error or provide an error template
        messages.error(request, 'Semothing went wrong ')
        return render(request, "user_templates/error.html", context)


# Here we are storing the data of Student of Personal Info using POST method
def create_personal_info(request):
    if request.method == 'POST':
        student = request.user
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        date_of_birth_str = request.POST.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        zip_code_str = request.POST.get('zip_code')
        try:
            zip_code = int(zip_code_str)
        except:
            zip_code = None
        objectives = request.POST.get('objectives')
        profile_picture = request.FILES.get('profile_picture')
        student_college_id = request.POST.get('student_id')

        try:
            p_obj = PersonalInfo(student=student, first_name=first_name, middle_name=middle_name,
                                 last_name=last_name, date_of_birth=date_of_birth, phone_number=phone_number,
                                 address=address, zip_code=zip_code, objectives=objectives,
                                 profile_picture=profile_picture, student_college_id=student_college_id)
            p_obj.save()
            messages.success(request, 'Personal-information add successfully')
            return redirect('viewprofile')
        except IntegrityError as e:
            error_message = str(e).lower().strip()
            if 'unique constraint' in error_message and 'student_id' in error_message:
                messages.error(request,"You have already added your personal information. Use the update feature to make changes.")
            elif 'unique constraint' in error_message and 'student_college_id' in error_message:
                messages.error(request, 'Student ID already exist. Please choose different ones.')
            elif 'unique constraint' in error_message and 'phone_number' in error_message:
                messages.error(request, 'Phone Number already exist. Please choose different ones.')
            return redirect('viewprofile')
    messages.error(request, "You have already added your personal information. Use the update feature to make changes.")
    return render(request, 'user_templates/viewprofile.html')


# Here we are updating the data of Student of Personal Info using Update method
def update_personal_info(request, personal_info_id):
    personal_info = PersonalInfo.objects.get(id=personal_info_id)
    try:
        if request.method == 'POST':
            personal_info.first_name = request.POST.get('first_name')
            personal_info.middle_name = request.POST.get('middle_name')
            personal_info.last_name = request.POST.get('last_name')
            personal_info.date_of_birth = request.POST.get('date_of_birth')
            personal_info.phone_number = request.POST.get('phone_number')
            personal_info.address = request.POST.get('address')
            personal_info.zip_code = request.POST.get('zip_code')
            personal_info.objectives = request.POST.get('objectives')
            personal_info.profile_picture = request.FILES.get('profile_picture')
            personal_info.student_college_id = request.POST.get('student_college_id')
            personal_info.save()
            messages.success(request, 'Personal-info update successfully')
            return redirect('profile')  # Redirect to the profile page or wherever you'd like
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'update_personal_info.html', {'personal_info': personal_info})
    except:
        messages.error(request, ' Something went wrong')
        return redirect('profile')


""" Here we are deleting the data of Student of Personal Info using Delete method """
def delete_personal_info(request, personal_info_id):
    personal_info = PersonalInfo.objects.get(id=personal_info_id)
    try:
        if request.method == 'POST':
            personal_info.delete()
            return redirect('profile')
        return render(request, 'delete_personal_info.html', {'personal_info': personal_info})
    except:
        messages.error(request, " Something went wrong")
        return redirect('profile')


""" Upload Resume View Here """
def Upload_Resume(request):
    user = request.user

    try:
        existing_resume = Resume.objects.get(user=user)
    except Resume.DoesNotExist:
        existing_resume = None

    if request.method == 'POST':
        # Get the uploaded resume file from the form
        resume = request.FILES['cv']

        # If an existing resume exists, delete it
        if existing_resume:
            path_to_delete = existing_resume.resume_file.path
            os.remove(path_to_delete)
            existing_resume.delete()

        # Create a new Resume object and save it
        new_resume = Resume(user=user, resume_file=resume)
        new_resume.save()
        messages.success(request, 'Upload Resume successfully!')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong! Please contact Admin')
    return render(request, 'user_templates/viewprofile.html')


"""  Delete Resume fuction here """
def Delete_Resume(request,id):
    try:
        delete_resume = Resume.objects.get(user__id=id)
        resume_path = delete_resume.resume_file.path
        os.remove(resume_path)
        delete_resume.delete()
        messages.success(request, "Resume delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, "Something went wrong! Please contact Admin")
        return redirect('viewprofile')


""" Experience Fuction handle here """
def Experience_Information(request):
    try:
        if request.method == 'POST':
            user = request.user
            job_type = request.POST.get('employment_type')
            company_name = request.POST.get('company_name')
            m_salary = request.POST.get('m_salary')
            location = request.POST.get('location')
            working_from = request.POST.get('working_from')
            working_till = request.POST.get('working_till')
            designation = request.POST.get('designation')
            role_responsibility = request.POST.get('rr')

            experience = Experience(user=user, job_type=job_type, company_name=company_name, monthly_salary=m_salary,
                                    designation=designation, location=location, working_till=working_till,
                                    working_from=working_from, description=role_responsibility)
            experience.save()
            messages.success(request, 'Experience-information add successfully!')
            return redirect('viewprofile')
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('viewprofile')


"""  Education Function are here """
def Education_Information(request):
    try:
        if request.method == 'POST':
            user = request.user
            institution_name = request.POST.get('i_name')
            field_of_study = request.POST.get('fos')
            start_date = request.POST.get('sd')
            end_date = request.POST.get('ed')
            department = request.POST.get('dn')
            cgpa = request.POST.get('cgpa')
            description = request.POST.get('des')

            education = Education(user=user, institution_name=institution_name, field_of_study=field_of_study, cgpa=cgpa,
                                start_date=start_date, end_date=end_date, description=description, department=department)
            education.save()
            messages.success(request, 'Education-information add successfully')
            return redirect('viewprofile')
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('viewprofile')

""" Certificate Fucntion are here"""
def Certification_Information(request):
    try:
        if request.method == 'POST':
            user = request.user
            certification_title = request.POST.get('certification_name')
            issue_organization = request.POST.get('issue-organization')
            issue_date = request.POST.get('i_d')
            certification_link = request.POST.get('c_l')
            description = request.POST.get('desc')

            certification = Certificate(user=user, title=certification_title, issuing_organisation=issue_organization,
                                        issue_date=issue_date, certificate_link=certification_link, description=description)
            certification.save()
            messages.success(request, 'Certification-information add successfully')
            return redirect('viewprofile')
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')
    except:
        messages.error(request, 'Something went wrong please try again')
        return redirect('viewprofile')

def Projects_Information(request):
    try:
        if request.method == 'POST':
            user = request.user
            project_title = request.POST.get("title")
            guide_name = request.POST.get("guide_name")
            start_date = request.POST.get("std")
            end_date = request.POST.get("ede")
            description = request.POST.get("desc")

            project = Project(user=user, title=project_title, advisor_name=guide_name, start_date=start_date,
                            end_date=end_date, description=description)
            project.save()
            messages.success(request, 'Project-information add successfully')
            return redirect('viewprofile')
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')
    except:
        messages.error(request, 'Something went wrong Please try again')
        return redirect('viewprofile')

""" Additional function are here """
def Additional_Skill(request):
    try:
        if request.method == 'POST':
            user = request.user
            hobbies_name = request.POST.get('ij')
            language = request.POST.get('lan')
            skill_name = request.POST.get('s_name')

            additional_skill = AdditionalSkill(user=user, hobbies_name=hobbies_name, language_name=language, skill_name=skill_name)
            additional_skill.save()
            messages.success(request, 'Additional-skill add successfully')
            return redirect('viewprofile')
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')
    except:
        messages.error(request, ' Something went wrong Please try again')


""" Download resume function here """
def Download_Resume(request,id):
    try:
        document = get_object_or_404(Resume, user__id=id)
        response = HttpResponse(document.resume_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.resume_file.name}"'
        return response
        messages.success(request,'Download-resume Successfully')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')


# def job_search(request):
#     query = request.GET.get('company-name')
#     location = request.GET.get('location')
#
#     jobs = JobPosting.objects.all()
#
#     if query:
#         jobs = jobs.filter(job_title__icontains=query)
#     if location:
#         jobs = jobs.filter(location=location)
#
#     context = {'show_job': jobs}
#     return render(request, 'user_templates/home.html', context)


@login_required
def New_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        try:
            # Check if the old password is correct
            if authenticate(username=user.username, password=old_password):
                # Check if the new password and confirm password match
                if new_password == confirm_password:
                    # Set the new password
                    user.set_password(new_password)
                    user.save()

                    # Update the session to prevent the user from being logged out
                    update_session_auth_hash(request, user)

                    messages.success(request, 'Password changed successfully.')
                    return redirect('home')
                else:
                    messages.error(request,'New password and confirm password do not match.')
                    return redirect('home')

            else:
                raise ValueError('Incorrect old password.')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'user_templates/new_password.html')