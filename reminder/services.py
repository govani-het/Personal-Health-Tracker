from datetime import datetime, UTC
from .models import Reminder
from .exceptions import *
from user.models import UserData


def add_reminder(*, user: UserData, reminder_title: str, reminder_description: str,
                 reminder_time: datetime) -> Reminder:
    if reminder_time < datetime.now(UTC):
        raise ReminderInPastError("Reminder date and time cannot be in the past.")

    reminder = Reminder.objects.create(user=user, reminder_title=reminder_title,
                                       reminder_description=reminder_description, datetime=reminder_time)

    return reminder


def get_reminder(user: UserData) -> Reminder:
    try:
        reminder = Reminder.objects.filter(user=user)
        return reminder
    except Reminder.DoesNotExist:
        raise ReminderInPastError("Reminder does not exist.")


def delete_reminder(id: int):
    try:

        reminder = Reminder.objects.get(id=id)
        reminder.delete()
        return {"success" : True,"message": "Reminder Deleted"}
    except Reminder.DoesNotExist:
        return {"message": "Reminder does not exist."}
