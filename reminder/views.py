from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status

from django.utils.decorators import method_decorator
from user.models import UserData
from .exceptions import *
from .models import Reminder
from .serializers import ReminderSerializer
from rest_framework.views import APIView
from . import services
from user.login_view import login_required

@login_required()
def load_reminder_page(request):
    return render(request,'reminder.html')


@method_decorator(login_required(), name='dispatch')
class ReminderView(APIView):

    def post(self, request):

        serializer = ReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        user = request.session.get('user_id')

        user_instence = UserData.objects.get(user_id=user)
        try:
            reminder = services.add_reminder(
                user=user_instence,
                reminder_title = validated_data['reminder_title'],
                reminder_description = validated_data['reminder_description'],
                datetime = validated_data['datetime'],
            )


        except ReminderInPastError as e:

            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response = ReminderSerializer(reminder)

        return Response(response.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.session.get('user_id')
        user_instence = UserData.objects.get(user_id=user)

        try:
            reminder = services.get_reminder(user_instence)
            response = ReminderSerializer(reminder,many=True)
            return Response(response.data, status=status.HTTP_200_OK)

        except ReminderInPastError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            reminder = services.delete_reminder(pk)
            return Response(reminder)
        except:
            return Response({'detail': "Something is wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):

        reminder_instance = Reminder.objects.get(pk=pk)
        serializer = ReminderSerializer(instance=reminder_instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)