from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Profile


@receiver(post_save, sender=Profile)
def send_signup_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Let's get started 🎉 "
        message = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 18px;
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
            <h1>Welcome to TaskX!</h1>
            <p>Dear {instance.user.first_name} {instance.user.last_name},</p>
                <p>Thank you for signing up for TaskX! We're excited to have you join our platform.</p>
                <p>With TaskX, you can easily manage your tasks, collaborate with your team, and stay organized.</p>
                <p>If you have any questions or need assistance, feel free to reach out to our support team.</p>
            <p>Happy task managing!</p>
            <p>Best regards,<br>TaskX Team</p>
        </body>
        </html>
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        try:
            send_mail(subject, message, from_email, recipient_list, html_message=message)
        except Exception as e:
            print(e)

            
