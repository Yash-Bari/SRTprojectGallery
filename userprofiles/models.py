from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    email = models.EmailField(unique=True)
    department_name = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=50)
    skills = models.TextField()
    linkedin_handler = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    demo_video = models.FileField(upload_to='project_demo_videos/')
    source_code_link = models.URLField()

    def __str__(self):
        return self.title
