from datetime import datetime
from .models import Reminder
from .exceptions import *
from user.models import UserData

def add_reminder(*, user: UserData, reminder_title: str, reminder_description: str, datetime: datetime) -> Reminder:

    if datetime < datetime.now():
        raise ReminderInPastError("Reminder date and time cannot be in the past.")

    reminder = Reminder.objects.create(user=user, reminder_title=reminder_title, reminder_description=reminder_description, datetime=datetime)

    return reminder

def get_reminder(user:UserData) -> Reminder:
    try:
        reminder = Reminder.objects.filter(user=user)
        return reminder
    except Reminder.DoesNotExist:
        raise ReminderInPastError("Reminder does not exist.")

def delete_reminder(id: int):
    try:
        reminder = Reminder.objects.get(id=id)
        reminder.delete()
        return True
    except Reminder.DoesNotExist:
        raise ReminderInPastError("Reminder does not exist.")

