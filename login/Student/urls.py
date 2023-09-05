
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePage, name='home'),
    path("viewprofile", ViewProfile, name='viewprofile'),
    path("personal-info", create_personal_info, name="personal-info"),
    path("job-description/<int:id>", Job_Description, name="job-description"),
    path("interest/<int:job_id>", job_application, name="interest"),
    path("upload-resume", Upload_Resume, name="upload-resume"),
    path("experience", Experience_Information, name='experience'),
    path("education", Education_Information, name='education'),
    path("certification", Certification_Information, name='certification'),
    path("projects", Projects_Information, name='projects'),
    path("additional-skill", Additional_Skill, name='additional-skill'),
    path("delete-resume/<int:id>", Delete_Resume, name='delete-resume'),
    path("download-resume/<int:id>", Download_Resume, name='download-resume'),
    path('status/', status_page, name='status_page'),

    # this path check validator user email & student_college_id
    path("check-user-email", Check_User_Email, name='check-user-email'),
    path("check-student-id", Check_Student_ID, name='check-student-id'),
    path("check-phone", Check_Phone, name='check-phone'),
    # path('job-search', job_search, name='job-search'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

