from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from app.models import JobPosting
import logging
import uuid


# This is for maintain a record when the Student will be  created or  updated his/her details
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, editable=False, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(TimeStampedModel, self).save(*args, **kwargs)


# we are store Student Personal Information here.
class PersonalInfo(TimeStampedModel):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, validators=[MinLengthValidator(limit_value=10)], unique=True)
    address = models.TextField(blank=True, null=True, max_length=1000)
    zip_code = models.IntegerField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True, max_length=1000)
    profile_picture = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    student_college_id = models.CharField(max_length=30, blank=True, null=True, unique=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return f"{self.First_name} {self.Last_name}"


# we are store Student Education here
class Education(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=25, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=500, blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return f"{self.user.username}"


# we are store Student Projects here
class Project(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    advisor_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    technologies_used = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return self.title


# we are store Student Experience here
class Experience(TimeStampedModel):
    choices = [
        ('internship', "Internship"),
        ('full_time', "Full Time")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=20, blank=True, null=True, choices=choices, default='full_time')
    company_name = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    working_from = models.DateField(blank=True, null=True)
    working_till = models.DateField(blank=True, null=True)
    monthly_salary = models.IntegerField(blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return f"{self.user.username}'s experience at {self.company_name}"


# we are store Student Certificate here.
class Certificate(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    issuing_organisation = models.CharField(max_length=200, blank=True, null=True)
    issue_date = models.DateField(blank=True, null=True)
    certificate_link = models.URLField(blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return self.title


# we are store Student Resume here
class Resume(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resume/')
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return f"{self.user.username}'s Resume"

    # we are store Student Hobbies and Acheivements here


class AdditionalSkill(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobbies_name = models.CharField(max_length=200, blank=True, null=True)
    language_name = models.CharField(max_length=200, blank=True, null=True)
    skill_name = models.CharField(max_length=200, blank=True, null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name='ID',
        help_text='Unique identifier for the record',
        db_index=True,
    )

    def _str_(self):
        return self.title


#  we are store Student Application here.
class Job_application(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    interested = models.BooleanField(default=False) # Set to True if interested False if not


