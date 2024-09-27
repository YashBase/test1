from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects')
    upload_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = (
        ('project_master', 'Project Master'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.user.username
    

class UploadedFile(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename
