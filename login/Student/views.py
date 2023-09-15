import os
from app.models import JobPosting
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from datetime import datetime
from django.db import IntegrityError
from xhtml2pdf import pisa
import qrcode
from PIL import Image
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate
from app.models import SelectedStudent


# Create your views here.
def Check_User_Email(request):
    if request.method == 'GET':
        email = request.GET['email_id']
        check_email = PersonalInfo.objects.filter(email=email)
        if len(check_email) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def Check_Student_ID(request):
    if request.method == 'GET':
        std_id = request.GET['student_college_id']
        check_std_id = PersonalInfo.objects.filter(student_college_id=std_id)
        if len(check_std_id) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


def Check_Phone(request):
    if request.method == 'GET':
        phone = request.GET['phone']
        check_phone = PersonalInfo.objects.filter(phone_number=phone)
        if len(check_phone) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")


# User Home_page
@login_required(login_url='login')
def HomePage(request):
    try:
        try:
            check_personal = PersonalInfo.objects.get(student_id=request.user.id)
        except PersonalInfo.DoesNotExist:
            check_personal = None
        try:
            check_resume = Resume.objects.get(user__id=request.user.id)
        except Resume.DoesNotExist:
            check_resume = None
        show_job = JobPosting.objects.all().order_by("-id")
        profile_image = UserProfile.objects.filter(user__id=request.user.id)
        check_additional = AdditionalSkill.objects.filter(user__id=request.user.id)
        applied_jobs = Job_application.objects.filter(user=request.user)
        applied_jobs_ids = [job.job_posting_id for job in applied_jobs]
        context = {
            'show_job': show_job,
            'applied_jobs_ids': applied_jobs_ids,
            'profile_image': profile_image,
            'check_additional': check_additional,
            'check_personal': check_personal,
            'check_resume': check_resume,
        }
        return render(request, 'user_templates/home.html', context)
    except Exception as e:
        messages.error(request, e)
        return render(request, 'user_templates/home.html')


# User View_Profile Page
@login_required(login_url='login')
def ViewProfile(request):
    try:
        user = request.user.id
        profile_image = UserProfile.objects.filter(user__id=user)
        personal_info = PersonalInfo.objects.filter(student__id=user)
        cv = Resume.objects.filter(user__id=user)
        experience = Experience.objects.filter(user__id=user).order_by("-id")
        education = Education.objects.filter(user__id=user).order_by("-id")
        certification = Certificate.objects.filter(user__id=user).order_by("-id")
        project = Project.objects.filter(user__id=user).order_by("-id")
        additional_skill = AdditionalSkill.objects.filter(user__id=user).order_by("-id")
        semester_college = SemesterCollege.objects.filter(user__id=user).order_by("-id")
        research = Research.objects.filter(user__id=user).order_by("-id")
        extra_curriculum = ExtraCurriculumAndAward.objects.filter(user__id=user).order_by("-id")
        context = {
            'personal_infos': personal_info,
            'profile_image': profile_image,
            'cvs': cv,
            'experience': experience,
            'education': education,
            'certification': certification,
            'project': project,
            'additional_skill': additional_skill,
            'semester_college': semester_college,
            'research': research,
            'extra_curriculum': extra_curriculum
        }
        return render(request, 'user_templates/viewprofile.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")  # Display the error message
        return render(request, 'user_templates/viewprofile.html')


"""Student show Interest View Here."""


@login_required(login_url='login')
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
        messages.error(request, 'Something went wrong')
        return redirect('home')


"""  Job Description Views Here ."""


@login_required(login_url='login')
def Job_Description(request, id):
    try:
        try:
            check_personal = PersonalInfo.objects.get(student_id=request.user.id)
        except PersonalInfo.DoesNotExist:
            check_personal = None
        try:
            check_resume = Resume.objects.get(user__id=request.user.id)
        except Resume.DoesNotExist:
            check_resume = None
        job_description = JobPosting.objects.get(id=id)
        applied_jobs = Job_application.objects.filter(user=request.user)
        applied_jobs_ids = [job.job_posting_id for job in applied_jobs]
        context = {
            "job_description": job_description,
            "applied_jobs_ids": applied_jobs_ids,
            'check_personal': check_personal,
            'check_resume': check_resume,
        }
        return render(request, "user_templates/job_description.html", context)
    except Exception as e:
        # Handle other exceptions here, e.g., log the error or provide an error template
        messages.error(request, 'Something went wrong. Please contact admin ')
        return render(request, "user_templates/error.html", context)


"""  Here we are storing the data of Student of Personal Info using POST method """


@login_required(login_url='login')
def create_personal_info(request):
    if request.method == 'POST':
        student = request.user
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        date_of_birth_str = request.POST.get('date_of_birth')
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin')
        if linkedin_url:
            # Generate the QR code
            qr_code = qrcode.QRCode(version=1, box_size=10, border=4)
            qr_code.add_data(linkedin_url)
            qr_code.make(fit=True)

            # Create an image from the QR code
            qr_image = qr_code.make_image(fill_color="blue", back_color="white")

            # Load the LinkedIn logo image
            logo_image = Image.open("static/images/linkedin.png")

            # Resize the logo image to a smaller size
            logo_size = (qr_image.size[0] // 4, qr_image.size[1] // 4)
            logo_image = logo_image.resize(logo_size)

            # Calculate the position to place the logo in the center of the QR code
            logo_position = ((qr_image.size[0] - logo_image.size[0]) // 2, (qr_image.size[1] - logo_image.size[1]) // 2)

            # Paste the logo image onto the QR code image
            qr_image.paste(logo_image, logo_position)

        address = request.POST.get('address')
        zip_code_str = request.POST.get('zip_code')
        try:
            zip_code = int(zip_code_str)
        except:
            zip_code = None
        objectives = request.POST.get('objectives')
        student_college_id = request.POST.get('student_id')
        try:
            p_obj = PersonalInfo(student=student, first_name=first_name, middle_name=middle_name,
                                 last_name=last_name, date_of_birth=date_of_birth, phone_number=phone_number,
                                 address=address, zip_code=zip_code, objectives=objectives,
                                 student_college_id=student_college_id, linkdin_url=linkedin_url)
            p_obj.save()
            # Save the final QR code image
            folder_path = "media/linkedinQR"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Save the image inside the folder with the user's first_name
            image_name = f"linkedin{first_name}.png"  # Or any desired image format
            image_path = os.path.join(folder_path, image_name)
            qr_image.save(image_path)
            messages.success(request, 'Personal-information added successfully')
            return redirect('viewprofile')
        except IntegrityError as e:
            error_message = str(e).lower().strip()
            if 'unique constraint' in error_message and 'student_id' in error_message:
                messages.error(request,"You have already added your personal information. Use the update feature to make changes.")
            elif 'unique constraint' in error_message and 'student_college_id' in error_message:
                messages.error(request, 'Student ID already exist. Please choose different ones.')
            elif 'unique constraint' in error_message and 'student_college_id' in error_message \
                    and 'phone_number' in error_message and 'email' in error_message:
                messages.error(request,
                               'Student_college_id & phone_number & email already exists. Please choose another one')
            elif 'unique constraint' in error_message and 'phone_number' in error_message:
                messages.error(request, 'Phone Number already exist. Please choose different ones.')
            elif 'unique constraint' in error_message and 'email' in error_message:
                messages.error(request, 'Email ID already exist. Please choose different ones.')
            elif 'unique constraint' in error_message and 'linkdin_url' in error_message:
                messages.error(request, 'Already exist. Please choose different ones.')
            return redirect('viewprofile')
    messages.error(request, "You have already added your personal information. Use the update feature to make changes.")
    return render(request, 'user_templates/viewprofile.html')


# Here we are updating the data of Student of Personal Info using Update method
def Update_Personal_Info(request, id):
    personal_info = PersonalInfo.objects.get(id=id)
    if request.method == 'POST':
        personal_info.first_name = request.POST.get('first_name')
        personal_info.middle_name = request.POST.get('middle_name')
        personal_info.last_name = request.POST.get('last_name')
        personal_info.date_of_birth = request.POST.get('date_of_birth')
        personal_info.phone_number = request.POST.get('phone_number')
        personal_info.address = request.POST.get('address')
        personal_info.linkdin_url = request.POST.get('linkedin_url')
        personal_info.zip_code = request.POST.get('zip_code')
        personal_info.objectives = request.POST.get('objectives')
        personal_info.student_college_id = request.POST.get('student_college_id')
        personal_info.save()
        messages.success(request, 'Personal-info update successfully')
        return redirect('viewprofile')  # Redirect to the profile page or wherever you'd like
    messages.error(request, 'Something went wrong! Please contact Admin')
    return render(request, 'user_templates/viewprofile.html')


# Here we are deleting the data of Student of Personal Info using Delete method
@login_required(login_url='login')
def Delete_Personal_Info(request, id):
    try:
        personal_info = PersonalInfo.objects.get(id=id)
        personal_info.delete()
        messages.success(request, "Personal_info delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


""" Upload Resume View Here """


@login_required(login_url='login')
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


@login_required(login_url='login')
def Delete_Resume(request,id):
    try:
        delete_resume = Resume.objects.get(id=id)
        resume_path = delete_resume.resume_file.path
        os.remove(resume_path)
        delete_resume.delete()
        messages.success(request, "Resume delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, "Something went wrong! Please contact Admin")
        return redirect('viewprofile')


""" Experience Fuction handle here """


@login_required(login_url='login')
def Experience_Information(request):
    if request.method == 'POST':
        user = request.user
        job_type = request.POST.get('employment_type')
        company_name = request.POST.get('company_name')
        location = request.POST.get('location')
        working_from = request.POST.get('working_from')
        working_from_text = datetime.strptime(working_from, "%Y-%m").strftime("%b-%Y")
        working_till = request.POST.get('working_till')
        working_till_text = datetime.strptime(working_till, "%Y-%m").strftime("%b-%Y")
        if working_till == "":
            working_till = "Present"
        designation = request.POST.get('designation')
        role_responsibility = request.POST.get('rr')

        experience = Experience(user=user, job_type=job_type, company_name=company_name,
                                designation=designation, location=location, working_till=working_till,
                                working_from=working_from, working_from_text=working_from_text, working_till_text=working_till_text, description=role_responsibility)
        experience.save()
        messages.success(request, 'Experience-information added successfully!')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong')
    return redirect('viewprofile')


def Update_Experience(request, id):
    update_experience = Experience.objects.get(id=id)
    if request.method == 'POST':
        update_experience.job_type = request.POST.get('employment_type')
        update_experience.company_name = request.POST.get('company_name')
        update_experience.designation = request.POST.get('designation')
        update_experience.description = request.POST.get('rr')
        update_experience.location = request.POST.get('location')
        work_from = request.POST.get('working_from')
        update_experience.working_from = work_from
        update_experience.working_from_text = datetime.strptime(work_from, "%Y-%m").strftime("%b-%Y")
        working_till = request.POST.get('working_till')
        if working_till:
            working_till_text = datetime.strptime(working_till, "%Y-%m").strftime("%b-%Y")
        if working_till == "":
            working_till = "Present"
        update_experience.working_till = working_till
        update_experience.working_till_text = working_till_text
        update_experience.save()
        messages.success(request, 'Experience update successfully')
        return redirect('viewprofile')  # Redirect to the profile page or wherever you'd like
    messages.error(request, 'Something went wrong! Please contact Admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Experience(request, id):
    try:
        experience = Experience.objects.get(id=id)
        experience.delete()
        messages.success(request, "Experience delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


def Under_Graduation_Information(request):
    if request.method == 'POST':
        user = request.user
        institute_name_ssc = request.POST.get('institute_name_ssc')
        board_name_scc = request.POST.get('board_name_scc')
        start_date_ssc = request.POST.get('start_date_ssc')
        end_date_ssc = request.POST.get('end_date_ssc')
        percentage_ssc = request.POST.get('percentage_ssc')
        description_ssc = request.POST.get('description_ssc')

        institute_name_hsc = request.POST.get('institute_name_hsc')
        board_name_hsc = request.POST.get('board_name_hsc')
        field_of_study_hsc = request.POST.get('field_of_study_hsc')
        percentage_hsc = request.POST.get('percentage_hsc')
        start_date_hsc = request.POST.get('start_date_hsc')
        end_date_hsc = request.POST.get('end_date_hsc')
        description_hsc = request.POST.get('description_hsc')
        department_hsc = request.POST.get('department_hsc')

        Education.objects.create(
            user=user,
            institution_name=institute_name_ssc,
            board_name=board_name_scc,
            cgpa_percentage=percentage_ssc,
            start_date=end_date_ssc,
            end_date=start_date_ssc,
            description=description_ssc,
        )

        Education.objects.create(
            user=user,
            institution_name=institute_name_hsc,
            field_of_study=field_of_study_hsc,
            board_name=board_name_hsc,
            cgpa_percentage=percentage_hsc,
            start_date=start_date_hsc,
            end_date=end_date_hsc,
            description=description_hsc,
            department=department_hsc
        )
        messages.success(request, 'Education-information add successfully')


def Delete_Under_Graduation(request, id):
    try:
        previous_education = Education.objects.get(id=id)
        previous_education.delete()
        messages.success(request, "UnderGraduation delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


def Update_Under_Graduation(request, id):
    update_education = Education.objects.get(id=id)
    if request.method == 'POST':
        update_education.institution_name = request.POST.get('i_name')
        update_education.field_of_study = request.POST.get('fos')
        update_education.cgpa_percentage = request.POST.get('cgpa')
        update_education.start_date = request.POST.get('sd')
        update_education.end_date = request.POST.get('ed')
        update_education.description = request.POST.get('des')
        update_education.department = request.POST.get('dn')
        update_education.save()
        messages.success(request, 'Education update successfully')
        return redirect('viewprofile')  # Redirect to the profile page or wherever you'd like
    messages.error(request, 'Something went wrong! Please contact Admin')
    return render(request, 'user_templates/viewprofile.html')


def Certification_Information(request):
    if request.method == 'POST':
        user = request.user
        certification_title = request.POST.get('certification_name')
        issue_organization = request.POST.get('issue-organization')
        issue_date = request.POST.get('i_d')
        certification_link = request.POST.get('c_l')
        description = request.POST.get('desc')
        aadhar_card = request.FILES.get('aadhar_card')
        tenth_marksheet = request.FILES.get('tenth_marksheet')
        eleven_marksheet = request.FILES.get('eleven_marksheet')
        twelve_marksheet = request.FILES.get('twelve_marksheet')
        eight_semester_marksheet = request.FILES.get('eight_semester_marksheet')
        certification = Certificate(user=user, title=certification_title, issuing_organisation=issue_organization,
                                    issue_date=issue_date, certificate_link=certification_link,
                                    description=description, aadhar_card=aadhar_card,
                                    tenth_marksheet=tenth_marksheet, eleven_marksheet=eleven_marksheet,
                                    twelve_marksheet=twelve_marksheet, eight_semester_marksheet=eight_semester_marksheet)
        certification.save()
        messages.success(request, 'Certification-information add successfully')
        return redirect('viewprofile')
    messages.error(request, 'something went wrong')
    return render(request, 'user_templates/viewprofile.html')


def Post_Graduation_Information(request):
    if request.method == 'POST':
        user = request.user
        institute_name_degree = request.POST.get('institute_name_degree')
        field_of_study_degree = request.POST.get('field_of_study_degree')
        percentage_degree = request.POST.get('percentage_degree')
        start_date_degree = request.POST.get('start_date_degree')
        end_date_degree = request.POST.get('end_date_degree')
        department_degree = request.POST.get('department_degree')
        description_degree = request.POST.get('description_degree')

        institute_name_ssc = request.POST.get('institute_name_ssc')
        board_name_scc = request.POST.get('board_name_scc')
        start_date_ssc = request.POST.get('start_date_ssc')
        end_date_ssc = request.POST.get('end_date_ssc')
        percentage_ssc = request.POST.get('percentage_ssc')
        description_ssc = request.POST.get('description_ssc')

        institute_name_hsc = request.POST.get('institute_name_hsc')
        board_name_hsc = request.POST.get('board_name_hsc')
        field_of_study_hsc = request.POST.get('field_of_study_hsc')
        percentage_hsc = request.POST.get('percentage_hsc')
        start_date_hsc = request.POST.get('start_date_hsc')
        end_date_hsc = request.POST.get('end_date_hsc')
        description_hsc = request.POST.get('description_hsc')

        Education.objects.create(
            user=user,
            institution_name=institute_name_ssc,
            board_name=board_name_scc,
            cgpa_percentage=percentage_ssc,
            start_date=end_date_ssc,
            end_date=start_date_ssc,
            description=description_ssc,
        )

        Education.objects.create(
            user=user,
            institution_name=institute_name_hsc,
            board_name=board_name_hsc,
            field_of_study=field_of_study_hsc,
            cgpa_percentage=percentage_hsc,
            start_date=start_date_hsc,
            end_date=end_date_hsc,
            description=description_hsc,
        )

        Education.objects.create(
            user=user,
            institution_name=institute_name_degree,
            field_of_study=field_of_study_degree,
            cgpa_percentage=percentage_degree,
            start_date=start_date_degree,
            end_date=end_date_degree,
            description=description_degree,
            department=department_degree
        )
        messages.success(request, 'Post Graduation add successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Certification(request, id):
    try:
        certification = Certificate.objects.get(id=id)

        # Check if file fields have files associated with them
        aadhar_card_file = certification.aadhar_card
        tenth_marksheet_file = certification.tenth_marksheet
        eleven_marksheet_file = certification.eleven_marksheet
        twelve_marksheet_file = certification.twelve_marksheet
        eight_semester_marksheet_file = certification.eight_semester_marksheet

        # Delete the certificate object
        certification.delete()

        # Delete associated files if they exist
        for file_field in [
            aadhar_card_file,
            tenth_marksheet_file,
            eleven_marksheet_file,
            twelve_marksheet_file,
            eight_semester_marksheet_file,
        ]:
            if bool(file_field) and file_field.name and os.path.isfile(file_field.path):
                os.remove(file_field.path)

        messages.success(request, "Certification and Documents deleted successfully!")
        return redirect('viewprofile')
    except Certificate.DoesNotExist:
        messages.error(request, 'Certificate does not exist.')
    except Exception as e:
        messages.error(request, f'Something went wrong! Error: {str(e)}')
    return render(request, 'user_templates/viewprofile.html')


def Update_Certification(request, id):
    update_certification = Certificate.objects.get(id=id)
    if request.method == 'POST':
        update_certification.title = request.POST.get('certification_name')
        update_certification.description = request.POST.get('desc')
        update_certification.issuing_organisation = request.POST.get('issue-organization')
        update_certification.issue_date = request.POST.get('i_d')
        update_certification.certificate_link = request.POST.get('c_l')
        update_certification.save()
        messages.success(request, 'Update certification Successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


""" Project Function are here """


@login_required(login_url='login')
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
    except Exception as e:
        messages.error(request, f'Please fill proper details. {e}')
        return redirect('viewprofile')


def Update_Project(request, id):
    update_project = Project.objects.get(id=id)
    if request.method == 'POST':
        update_project.title = request.POST.get('title')
        update_project.advisor_name = request.POST.get('guide_name')
        update_project.description = request.POST.get('desc')
        update_project.start_date = request.POST.get('std')
        update_project.end_date = request.POST.get('ede')
        update_project.save()
        messages.success(request, 'Update project detail successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Project(request, id):
    try:
        project = Project.objects.get(id=id)
        project.delete()
        messages.success(request, "Project delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


""" Additional function are here """


@login_required(login_url='login')
def Additional_Skill(request):
    try:
        if request.method == 'POST':
            user = request.user
            hobbies_name = request.POST.get('ij')
            language = request.POST.get('lan')
            skill_name = request.POST.get('s_name')

        additional_skill = AdditionalSkill(user=user, hobbies_name=hobbies_name, language_name=language,
                                           skill_name=skill_name)
        additional_skill.save()
        messages.success(request, 'Additional-skill add successfully')
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


def Update_AdditionalSkill(request, id):
    update_additional_skill = AdditionalSkill.objects.get(id=id)
    if request.method == 'POST':
        update_additional_skill.hobbies_name = request.POST.get('ij')
        update_additional_skill.language_name = request.POST.get('lan')
        update_additional_skill.skill_name = request.POST.get('s_name')
        update_additional_skill.save()
        messages.success(request, 'additional skill details update successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_AdditionalSkill(request, id):
    try:
        project = AdditionalSkill.objects.get(id=id)
        project.delete()
        messages.success(request, "AdditionalSkill delete successfully!")
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')
        return render(request, 'user_templates/viewprofile.html')


def Semester_College(request):
    if request.method == 'POST':
        user = request.user
        institute_name = request.POST.get('institute_name')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        sgpa = request.POST.get('sgpa')
        cgpa = request.POST.get('cgpa')

        semester_college = SemesterCollege(user=user, institute_name=institute_name, semester=semester,
                                           year=year, sgpa=sgpa, cgpa=cgpa)
        semester_college.save()
        messages.success(request, 'Semester information add successfully')
        return redirect('viewprofile')

    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Update_Semester_College(request, id):
    update_semester_college = SemesterCollege.objects.get(id=id)
    if request.method == 'POST':
        update_semester_college.institute_name = request.POST.get('institute_name')
        update_semester_college.semester = request.POST.get('semester')
        update_semester_college.year = request.POST.get('year')
        update_semester_college.sgpa = request.POST.get('sgpa')
        update_semester_college.cgpa = request.POST.get('cgpa')

        update_semester_college.save()
        messages.success(request, 'Semester detail update successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Semester_College(request, id):
    try:
        delete_semester_college = SemesterCollege.objects.get(id=id)
        delete_semester_college.delete()
        messages.success(request, 'Semester delete successfully')
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong. Please contact with admin')
        return render(request, 'user_templates/viewprofile.html')


def Research_info(request):
    if request.method == 'POST':
        user = request.user
        title_name = request.POST.get('title')
        supervisor = request.POST.get('supervisor')
        technologies_used = request.POST.get('tech')
        start_date = request.POST.get('start_date')
        start_date_text = datetime.strptime(start_date, "%Y-%m").strftime("%b-%Y")
        end_date = request.POST.get('end_date')
        end_date_text = datetime.strptime(end_date, "%Y-%m").strftime("%b-%Y")
        description = request.POST.get('description')

        research = Research(user=user, title=title_name, supervisor=supervisor, technologies_used=technologies_used,
                            start_date=start_date, end_date=end_date, start_date_text=start_date_text, end_date_text=end_date_text, description=description)
        research.save()
        messages.success(request, 'Research detail add successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return redirect(request, 'user_templates/viewprofile.html')


def Update_Research(request, id):
    update_research = Research.objects.get(id=id)
    if request.method == 'POST':
        update_research.title = request.POST.get('title')
        update_research.technologies_used = request.POST.get('tech')
        start_date = request.POST.get('start_date')
        update_research.start_date = start_date
        update_research.start_date_text = datetime.strptime(start_date, "%Y-%m").strftime("%b-%Y")
        end_date = request.POST.get('end_date')
        update_research.end_date = end_date
        update_research.end_date_text = datetime.strptime(end_date, "%Y-%m").strftime("%b-%Y")
        update_research.supervisor = request.POST.get('supervisor')
        update_research.description = request.POST.get('description')

        update_research.save()
        messages.success(request, 'Research detail update successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Extra_Curriculum(request):
    if request.method == 'POST':
        user = request.user
        award = request.POST.get('award')
        curriculum = request.POST.get('curriculum')

        extra_curriculum = ExtraCurriculumAndAward(user=user, award=award, curriculum=curriculum)
        extra_curriculum.save()
        messages.success(request, 'Extra curriculum detail add successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return redirect(request, 'user_templates/viewprofile.html')


def Update_Extra_Curriculum(request, id):
    update_extra_curriculum = ExtraCurriculumAndAward.objects.get(id=id)
    if request.method == 'POST':
        update_extra_curriculum.award = request.POST.get('award')
        update_extra_curriculum.curriculum = request.POST.get('curriculum')

        update_extra_curriculum.save()
        messages.success(request, 'Extra curriculum detail update successfully')
        return redirect('viewprofile')
    messages.error(request, 'Something went wrong. Please contact with admin')
    return render(request, 'user_templates/viewprofile.html')


def Delete_Extra_Curriculum(request, id):
    try:
        delete_extra_curriculum = ExtraCurriculumAndAward.objects.get(id=id)
        delete_extra_curriculum.delete()
        messages.success(request, 'Extra curriculum delete successfully')
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong. Please contact with admin')
        return render(request, 'user_templates/viewprofile.html')


def Delete_Research(request, id):
    try:
        delete_research = Research.objects.get(id=id)
        delete_research.delete()
        messages.success(request, 'research delete successfully')
        return redirect('viewprofile')
    except:
        messages.error(request, 'Something went wrong. Please contact with admin')
        return render(request, 'user_templates/viewprofile.html')


""" Download resume function here """


@login_required(login_url='login')
def Download_Resume(request,id):
    try:
        document = get_object_or_404(Resume, user__id=id)
        response = HttpResponse(document.resume_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{document.resume_file.name}"'
        return response
    except:
        messages.error(request, 'Something went wrong! Please contact Admin')


def Upload_Image(request):
    user = request.user
    try:
        existing_image = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        existing_image = None

    if request.method == 'POST':
        # Get the uploaded resume file from the form
        upload_file = request.FILES.get('file')

        # If an existing resume exists, delete it
        if existing_image:
            path_to_delete = existing_image.profile_picture.path
            os.remove(path_to_delete)
            existing_image.delete()
        obj = UserProfile(user=user, profile_picture=upload_file)
        obj.save()
        messages.success(request, 'Profile Save Successfully')
        return redirect('viewprofile')
    return render(request, 'user_templates/viewprofile.html')



def html_to_pdf_view(request):
    # Generate HTML content using a template or manually
    u = request.user.id
    user_data = PersonalInfo.objects.get(student__id=u)
    user_profile = UserProfile.objects.filter(user__id=u)
    education_data = Education.objects.filter(user=u).order_by('-id').first()
    education = Education.objects.filter(user=u)
    project = Project.objects.filter(user__id=u)
    experience = Experience.objects.filter(user__id=u,job_type='full_time')
    internship = Experience.objects.filter(user__id=u,job_type='internship')
    certification = Certificate.objects.filter(user__id=u)
    additional_skill = AdditionalSkill.objects.filter(user__id=u)
    resarch = Research.objects.filter(user__id=u)
    sem_college = SemesterCollege.objects.filter(user__id=u).values_list('semester','year','sgpa','cgpa')
    sem_college_name = SemesterCollege.objects.filter(user__id=u)[0]
    award = ExtraCurriculumAndAward.objects.filter(user__id=u,award__isnull=False)
    curriculum = ExtraCurriculumAndAward.objects.filter(user__id=u,curriculum__isnull=False)


    # sem_data ={}

    semester =[]
    if education.count() == 3:
        semester.extend([sem_college[0]+sem_college[2]])
        semester.extend([sem_college[1]+sem_college[3]])
    elif education.count() == 2:
        semester.extend([sem_college[0] + sem_college[4]])
        semester.extend([sem_college[1] + sem_college[5]])
        semester.extend([sem_college[2] + sem_college[6]])
        semester.extend([sem_college[3] + sem_college[7]])

    context = {
        'user_data': user_data,
        'user_profile': user_profile,
        'education_data': education_data,
        'education': education,
        'project': project,
        'experience': experience,
        'internship':internship,
        'certification': certification,
        'additional_skill': additional_skill,
        'education_details': education,
        'resarch':resarch,
        'sem_data':semester,
        'sem_college_name':sem_college_name,
        'curriculum':curriculum,
        'award':award,
    }

    html_content = render_to_string('user_templates/resume_make.html', context)

    # Create a PDF from the HTML content
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'
    pisa.CreatePDF(html_content, dest=response)
    return response


def download_resume(request):
    return render(request, 'user_templates/index2.html')


@login_required(login_url='login')
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


# selected student show here
def status_page(request):
    selected_students = SelectedStudent.objects.filter(selected=True)
    return render(request, 'user_templates/status.html', {'selected_students': selected_students})




# search company names

# def job_search(request):
#     if request.method == "GET":
#         company_name = request.GET.get("company-name", "")
#         location = request.GET.get("employment-type", "")

#         # Filter jobs based on company name and location and extract company names
#         matching_company_names = JobPosting.objects.filter(company_name__icontains=company_name, location__icontains=location).values_list('company_name', flat=True)

#         # Create a comma-separated string of matching company names
#         company_names_str = ", ".join(matching_company_names)

#         # Return the matching company names as plain text
#         return HttpResponse(company_names_str)
