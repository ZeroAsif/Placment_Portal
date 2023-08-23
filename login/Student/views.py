from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models import JobPosting
from django.shortcuts import render, redirect
from .models import PersonalInfo, Job_application, User, Resume
import uuid
from django.shortcuts import get_object_or_404,HttpResponse


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
        personal_info = PersonalInfo.objects.get(student_id=user)
        # resume = Resume.objects.get(user_id=user)
        context = {
            "personal_info": personal_info,
            # "resume": resume,
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


"""Here we are updating the data of Student of Personal Info using Update method"""


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


"""Here we are deleting the data of Student of Personal Info using Delete method"""


def delete_personal_info(request, personal_info_id):
    personal_info = PersonalInfo.objects.get(id=personal_info_id)
    if request.method == 'POST':
        personal_info.delete()
        return redirect('profile')
    return render(request, 'delete_personal_info.html', {'personal_info': personal_info})


def create_student_skills(request):
    if request.method == 'POST':
        skill_data = {
            'user': request.user,
            'skill_name': request.POST.get('skill_name'),
            'id': uuid.uuid4()
        }
        StudentSkill.objects.create(**skill_data)
        return redirect('profile')
    return render(request, 'create_student_skill.html')


def update_student_skills(request, student_skill_id):
    student_skill = StudentSkill.objects.get(id=student_skill_id)
    if request.method == 'POST':
        student_skill.skill_name = request.POST.get('skill_name')
        student_skill.save()
        return redirect('student_skill')
    return render(request, 'update_student_skills.html')


def delete_student_skill(request, student_skill_id):
    student_skill = StudentSkill.objects.get(id=student_skill_id)
    if request.method == 'DLETE':
        student_skill.delete()
        return redirect('student skill')
    return render(request, 'delete_student_skill')


def create_language_skill(request):
    if request.method == 'POST':
        try:
            language_skills = {
                'student': request.user,
                'language_name': request.POST.get('language_name'),
                'id': uuid.uuid4()
            }
            LanguageSkill.objects.create(**language_skills)
            return redirect('profile')  # Redirect to the profile page or wherever you'd like

        except Exception as e:
            error_message = f"An error occurred: {e}"
            # Handle the error or log it as needed

    return render(request, 'create_language_skill.html')


def update_language_skill(request, language_skill_id):
    language_skills = LanguageSkill.objects.get(id=language_skill_id)
    if request.method == 'POST':
        try:
            LanguageSkill.language_name = request.POST.get('language_name')
            LanguageSkill.save()
            return redirect('profile')  # Redirect to the profile page or wherever you'd like

        except Exception as e:
            error_message = f"An error occurred: {e}"
            # Handle the error or log it as needed

    return render(request, 'update_language_skill.html', {'language_skill': language_skills})


def delete_language_skill(request, language_skill_id):
    language_skills = LanguageSkill.objects.get(id=language_skill_id)
    if request.method == 'Delete':
        try:
            language_skills.delete()
            return redirect('')
        except Exception as e:
            error_message = f"An error occured:{e}"
    return render(request, '', {'language_skills': language_skills})


# def Upload_Resume(request):
#     user_id = User.objects.get(id=request.user.id)
#     if request.method == 'POST':
#         resume = request.POST.get('resume')
#         obj = Resume(user=user_id, resume_file=resume)
#         obj.save()
#         return redirect('viewprofile')
#     return render(request, 'user_templates/viewprofile.html')
#
#
# def Download_Resume(request,id):
#         document = get_object_or_404(Resume, id=id)
#         response = HttpResponse(document.file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
#         return response


# job search
def Job_Search(request):
    designation = request.GET.get('company-name')
    location = request.GET.get('employment-type')

    jobs = JobPosting.objects.all()

    if designation:
        jobs = jobs.filter(job_title__icontains=designation)

    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'user_templates/home.html', {'jobs':jobs})
