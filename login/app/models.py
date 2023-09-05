from django.db import models
from django.contrib.auth.models import User


class JobPosting(models.Model):
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    HIRING_STATUS_CHOICES = [
        ('hiring', 'Hiring'),
        ('hiring_closed', 'Hiring Closed'),
    ]
    hiring_status = models.CharField(max_length=20, choices=HIRING_STATUS_CHOICES, default='hiring')
    salary_range = models.CharField(max_length=50)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
   
    

    

class SelectedStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ... Your existing fields ...
    company_name = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    selected = models.BooleanField(default=False)  
    message = models.CharField(max_length=255, blank=True, null=True, default="")

    def __str__(self):
         return f"{self.user.username} - {self.company_name}"
