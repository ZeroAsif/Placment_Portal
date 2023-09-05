
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePage, name='home'),
    path("viewprofile", ViewProfile, name='viewprofile'),
    path("personal-info", create_personal_info, name="personal-info"),
    path("job-description/<int:id>", Job_Description, name='job-description'),
    path("interest/<int:job_id>", job_application, name='interest'),
    path("upload-resume", Upload_Resume, name='upload-resume'),
    path("experience", Experience_Information, name='experience'),
    path("semester-college", Semester_College, name='semester-college'),
    path("previous-education", Under_Graduation_Information, name='previous-education'),
    path("post-education", Post_Graduation_Information, name='post-education'),
    path("certification", Certification_Information, name='certification'),
    path("projects", Projects_Information, name='projects'),
    path("additional-skill", Additional_Skill, name='additional-skill'),
    path("research", Research_info, name='research'),
    path("extra-curriculum", Extra_Curriculum, name='extra-curriculum'),
    path("download-resume/<int:id>", Download_Resume, name='download-resume'),
    path("upload-image", Upload_Image, name='upload-image'),

    # this update path section
    path("update-personal-info/<str:id>", Update_Personal_Info, name='update-personal-info'),
    path("update-experience/<str:id>", Update_Experience, name='update-experience'),
    path("update-under-graduation/<str:id>", Update_Under_Graduation, name='update-under-graduation'),
    path("update-certification-detail/<str:id>", Update_Certification, name='update-certification-detail'),
    path("update-project-detail/<str:id>", Update_Project, name='update-project-detail'),
    path("update-additional-skill/<str:id>", Update_AdditionalSkill, name='update-additional-skill'),
    path("update-semester-college/<str:id>", Update_Semester_College, name='update-semester-college'),
    path("update_research/<str:id>", Update_Research, name='update_research'),
    path("update-extra-curriculum/<str:id>", Update_Extra_Curriculum, name='update-extra-curriculum'),

    # This Delete path section
    path("delete-personal-info/<str:id>", Delete_Personal_Info, name='delete-personal-info'),
    path("delete-resume/<str:id>", Delete_Resume, name='delete-resume'),
    path("delete-experience/<str:id>", Delete_Experience, name='delete-experience'),
    path("delete-under-graduation/<str:id>", Delete_Under_Graduation, name='delete-under-graduation'),
    path("delete-certification/<str:id>", Delete_Certification, name='delete-certification'),
    path("delete-project/<str:id>", Delete_Project, name='delete-project'),
    path("delete-additional-skill/<str:id>", Delete_AdditionalSkill, name='delete-additional-skill'),
    path("delete-semester-college/<str:id>", Delete_Semester_College, name='delete-semester-college'),
    path("delete-research/<str:id>", Delete_Research, name='delete-research'),
    path("delete-extra-curriculum/<str:id>", Delete_Extra_Curriculum, name='delete-extra-curriculum'),

    # this path check validator user email & student_college_id
    path("check-user-email", Check_User_Email, name='check-user-email'),
    path("check-student-id", Check_Student_ID, name='check-student-id'),
    path("check-phone", Check_Phone, name='check-phone'),
    path("resume", download_resume, name='resume'),
    path("download", html_to_pdf_view, name='download')

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

