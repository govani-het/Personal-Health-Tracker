from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Reminder
from user.models import UserData

@shared_task
def send_reminder(reminder_id):
    try:
        reminder = Reminder.objects.filter(id=reminder_id).values(
            "id",
            "reminder_title",
            "reminder_description",
            "datetime",
            "active",
            "user__email",
        ).first()

        if reminder.active == 1:
            send_mail(
                subject=reminder["reminder_title"],
                message=reminder["reminder_description"],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[reminder["user__email"]],
                fail_silently=False,
            )
            reminder.active = 0
            reminder.save()
            return 'Reminder sent'

    except Reminder.DoesNotExist:
        return f"Notification {id} not found."
    except Exception as e:
        return f"Failed to send notification {id}: {e}"


@shared_task
def check_due_reminder():
    now = timezone.now()
    due_reminders = Reminder.objects.filter(
        datetime__lte=now,
        active=1,
    )

    for reminder in due_reminders:
        send_reminder.delay(reminder.id)

    return f"Checked for due notifications. Found and queued {due_reminders.count()}."