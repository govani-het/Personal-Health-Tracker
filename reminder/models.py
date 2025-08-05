from django.db import models
from user.models import UserData


class Reminder(models.Model):

    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    reminder_title = models.CharField(max_length=100)
    reminder_description = models.TextField()
    datetime = models.DateTimeField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} {} {}".format(self.user, self.reminder_title, self.reminder_description)

    def as_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'reminder_title': self.reminder_title,
            'reminder_description': self.reminder_description,
            'datetime': self.datetime,
            'active': self.active,
            'created_at': self.created_at,
            'updated_at': self.updated_at

        }

    class Meta:
        db_table = 'reminder'
