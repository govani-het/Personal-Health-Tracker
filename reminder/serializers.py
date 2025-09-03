from django.utils import timezone

from rest_framework import serializers

from reminder.models import Reminder


def validate_datetime(value):
    if value < timezone.now():
        raise serializers.ValidationError('The date cannot be in the past')

    return value


class ReminderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reminder
        fields = ['id', 'reminder_title', 'reminder_description', 'datetime', 'user']
