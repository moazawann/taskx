from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Task


@receiver(post_save, sender=Task)
def send_new_task_email(sender, instance, created, **kwargs):
    if created:
        subject = f'New Task Assigned: {instance.title}'
        message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 14px;
                    color: #333333;
                }}
                h1 {{
                    color: #0077b6;
                }}
                .info {{
                    background-color: #f2f2f2;
                    padding: 10px;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <h1>New Task Assigned</h1>
            <p>Hello,</p>
            <p>A new task has been assigned to you. Please find the details below:</p>
            
            <div class="info">
                <strong>Task Title:</strong> {instance.title}<br><br>
                <strong>Details:</strong> {instance.description}<br><br>
                <strong>Priority:</strong> {instance.get_priority_display()}<br><br>
                <strong>Status:</strong> {instance.get_status_display()}<br><br>
                <strong>Due Date:</strong> {instance.due_date}<br><br>
                <strong>Created By:</strong> {instance.created_by.user.username}
            </div>
            
            <p>Please take the necessary actions to complete this task on time.</p>
            <p>Best regards,<br>TaskX Team</p>
        </body>
        </html>
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.assigned_to.user.email]

        try:
            send_mail(subject, message, from_email, recipient_list, html_message=message)
        except Exception as e:
            print(e)

            
