
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
    path("resume",download_resume,name='resume'),
    path("resume-delete/<int:id>", Delete_Resume, name='resume-delete'),
    path("download",html_to_pdf_view,name='download'),
    # path("download/<int:id>", Download_Resume, name='download')
    # path('job-search', Job_Search, name='job-search'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

