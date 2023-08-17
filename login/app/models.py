from django.db import models
from django.contrib.auth.models import User

class JobPosting(models.Model):
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    application_deadline = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

