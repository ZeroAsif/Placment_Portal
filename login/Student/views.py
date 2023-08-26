import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import JobPosting
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from xhtml2pdf import pisa
from django.template.loader import render_to_string
import uuid
from django.shortcuts import get_object_or_404, HttpResponse


# Create your views here.


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


# Student show Interest View Here.
def job_application(request, job_id):
    job_posting = JobPosting.objects.get(id=job_id)

    # Check if an application for this job by the user already exists
    existing_application = Job_application.objects.filter(user=request.user, job_posting=job_posting).first()
    if existing_application:
        existing_application.interested = True
        existing_application.save()
    else:
        new_application = Job_application(user=request.user, job_posting=job_posting, interested=True)
        new_application.save()
    return redirect('home')


# Job Description Views Here.
def Job_Description(request, id):
    job_description = JobPosting.objects.get(id=id)
    applied_jobs = Job_application.objects.filter(user=request.user)
    applied_jobs_ids = [job.job_posting_id for job in applied_jobs]
    context = {
        "job_description": job_description,
        "applied_jobs_ids": applied_jobs_ids
    }
    return render(request, "user_templates/job_description.html", context)


# Here we are storing the data of Student of Personal Info using POST method
def create_personal_info(request):
    if request.method == 'POST':
        personal_info_data = {
            'student': request.user,
            'email': request.POST.get('email'),
            'first_name': request.POST.get('first_name'),
            'middle_name': request.POST.get('middle_name'),
            'last_name': request.POST.get('last_name'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'phone_number': request.POST.get('phone_number'),
            'address': request.POST.get('address'),
            'zip_code': request.POST.get('zip_code'),
            'objectives': request.POST.get('objectives'),
            'profile_picture': request.FILES.get('profile_picture'),
            'student_college_id': request.POST.get('student_id'),
        }
        p_obj = PersonalInfo.objects.create(**personal_info_data)
        return redirect('viewprofile')
    return render("request", 'user_templates/viewprofile.html')


# Here we are updating the data of Student of Personal Info using Update method
def update_personal_info(request, personal_info_id):
    personal_info = PersonalInfo.objects.get(id=personal_info_id)
    if request.method == 'POST':
        personal_info.email = request.POST.get('email')
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
        return redirect('profile')  # Redirect to the profile page or wherever you'd like
    return render(request, 'update_personal_info.html', {'personal_info': personal_info})


# Here we are deleting the data of Student of Personal Info using Delete method
def delete_personal_info(request, personal_info_id):
    personal_info = PersonalInfo.objects.get(id=personal_info_id)
    if request.method == 'POST':
        personal_info.delete()
        return redirect('profile')
    return render(request, 'delete_personal_info.html', {'personal_info': personal_info})


# Upload Resume View Here.
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
        return redirect('viewprofile')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Resume(request,id):
    delete_resume = Resume.objects.get(user__id=id)
    resume_path = delete_resume.resume_file.path
    os.remove(resume_path)
    delete_resume.delete()
    return redirect('viewprofile')


def Experience_Information(request):
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
        return redirect('viewprofile')

    return render(request, 'user_templates/viewprofile.html')


def Education_Information(request):
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
        return redirect('viewprofile')

    return render(request, 'user_templates/viewprofile.html')


def Certification_Information(request):
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
        return redirect('viewprofile')

    return render(request, 'user_templates/viewprofile.html')


def Projects_Information(request):
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
        return redirect('viewprofile')

    return render(request, 'user_templates/viewprofile.html')


def Additional_Skill(request):
    if request.method == 'POST':
        user = request.user
        hobbies_name = request.POST.get('ij')
        language = request.POST.get('lan')
        skill_name = request.POST.get('s_name')

        additional_skill = AdditionalSkill(user=user, hobbies_name=hobbies_name, language_name=language, skill_name=skill_name)
        additional_skill.save()
        return redirect('viewprofile')
    return render(request, 'user_templates/viewprofile.html')


# def Download_Resume(request,id):
#         document = get_object_or_404(Resume, id=id)
#         response = HttpResponse(document.file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
#         return response


# job search
# def Job_Search(request):
#     designation = request.GET.get('company-name')
#     location = request.GET.get('employment-type')
#
#     jobs = JobPosting.objects.all()
#
#     if designation:
#         jobs = jobs.filter(job_title__icontains=designation)
#
#     if location:
#         jobs = jobs.filter(location__icontains=location)
#
#     return render(request, 'user_templates/home.html', {'jobs':jobs})