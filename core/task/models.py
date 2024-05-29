from django.db import models
from accounts.models import Profile

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = (
        (1,'High'),
        (2,'Medium'),
        (3,'Low'),
    )
    STATUS_CHOICES = ( 
        (1, 'Completed'),
        (0,  'Pending'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='task_assignedto')
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='task_createdby')
    updated_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='task_updatedby')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def get_priority_label(self):
        return dict(self.PRIORITY_CHOICES)[self.priority]

    def get_status_label(self):
        return dict(self.STATUS_CHOICES)[self.status]
    

class Favourite(models.Model):
    task_id = models.ForeignKey(Task, on_delete= models.CASCADE, related_name='fav_task')
    profile_id = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name='fav_profile')
    favourite =models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
         return f"Task: {self.task_id.title}, Profile: {self.profile_id.user.username}"
    



class Comment(models.Model):
    task_id = models.ForeignKey(Task, on_delete= models.CASCADE, related_name='comment_task')
    profile_id = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name='comment_profile')
    comment = models.TextField()
    
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_createdby')
    updated_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_updatedby')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False)


    def __str__(self):
         return f" ID: {self.id}, Task: {self.task_id.title}, Profile: {self.profile_id.user.username}"





