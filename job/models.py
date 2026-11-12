from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):
    ROLE_CHOICES = [
        ('RECRUITER', 'Recruiter'),
        ('CANDIDATE', 'Candidate'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CANDIDATE')





class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    qualification = models.CharField(max_length=50)
    skills = models.TextField()
    experience = models.PositiveIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name






class Job(models.Model):
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("Closed", "Closed"),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField(help_text="Comma separated skills")
    location = models.CharField(max_length=50)
    experience = models.PositiveIntegerField(default=0)
    min_salary = models.DecimalField(max_digits=20, decimal_places=2)
    max_salary = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Open")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="jobs", null=True, blank=True)

    def __str__(self):
        return self.title





class Application(models.Model):
    APPLICATION_STATUS = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEW', 'Interview'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    ]

    status = models.CharField(max_length=50, choices=APPLICATION_STATUS, default='APPLIED')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.name} - {self.job.title} -{(self.job.created_by)}"