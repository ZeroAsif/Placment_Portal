
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
# from . import views

urlpatterns = [
     path('', SignupPage, name="signup"),
     path('login/', LoginPage, name="login"),
     path('logout/',LogoutPage,name='logout'),
     path('admins/',AdminPage,name='admins'),
     path('addjob/',Jobposting,name='addjob'),
     path('delete/<int:job_id>/', delete_job_posting, name='delete_job'),
     path('update/<int:job_id>/', update_job_posting, name='update_job'),
     path('forget-password/' , ForgetPassword , name="forget_password"),
     path('change-password/<token>/' , ChangePassword , name="change_password"),
     path('<int:job_id>/', ExportExcel, name='export_excels'),
     path('save_selected_students/',save_selected_students,name='save_selected_students'),
     path('verify_email/<str:uid>/<str:token>/', verify_email, name='verify_email'),
     path('check_email_page/', check_email, name='check_email_page'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


