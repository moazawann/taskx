from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_createdby')
    updated_by = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_updatedby')

    def __str__(self):
        return self.user.username

