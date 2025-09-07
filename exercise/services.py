import datetime

import requests
from django.conf import settings
from django.db.models import Sum

from .models import Exercise, Cardio, WeightLifting
from user.models import UserData
from . import exception

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"


def add_exercise(request):
    user_id = request.session.get('user_id')
    exercise_type = request.POST.get('exercise_type')
    exercise_name = request.POST.get('exercise_name')
    intensity = request.POST.get('intensity')

    duration = request.POST.get('duration')
    distance = request.POST.get('distance')

    exercise_set = request.POST.get('sets')
    weight = request.POST.get('weight')
    exercise_reps = request.POST.get('reps')

    try:
        user_instance = UserData.objects.get(user_id=user_id)
    except:
        raise exception.UserNotFound(f"CRITICAL ERROR: User with id {user_id} does not exist in the database.")

    if exercise_type == 'Cardio':

        exercise = f"{exercise_name} for {duration} min {distance} km with {intensity} intensity"

        header = {
            'x-app-id': settings.NUTRITIONIX_APP_ID,
            'x-app-key': settings.NUTRITIONIX_API_KEY,
            'x-remote-user-id': str(user_id)
        }

        payload = {
            "query": exercise,
        }

        response = requests.post(NUTRITIONIX_API_URL, headers=header, json=payload)

        response.raise_for_status()

        exercise_data = response.json()

        new_exercise = Exercise.objects.create(
            user=user_instance,
            exercise_type=exercise_type,
            exercise_name=exercise_name,
            intensity=intensity,
            kcal=exercise_data['exercises'][0]['nf_calories']
        )
        Cardio.objects.create(
            exercise=new_exercise,
            duration_minutes=duration,
            distance_km=distance,
        )

    elif exercise_type == 'Weight Lifting':
        exercise = f"{exercise_set} set of {exercise_reps}  {exercise_name} at {weight} with {intensity} intensity"

        header = {
            'x-app-id': settings.NUTRITIONIX_APP_ID,
            'x-app-key': settings.NUTRITIONIX_API_KEY,
            'x-remote-user-id': str(user_id)
        }

        payload = {
            "query": exercise,
        }

        response = requests.post(NUTRITIONIX_API_URL, headers=header, json=payload)

        response.raise_for_status()

        exercise_data = response.json()

        new_exercise = Exercise.objects.create(
            user=user_instance,
            exercise_type=exercise_type,
            exercise_name=exercise_name,
            intensity=intensity,
            kcal=exercise_data['exercises'][0]['nf_calories']
        )
        WeightLifting.objects.create(
            exercise=new_exercise,
            weight_kg=weight,
            sets=exercise_set,
            reps=exercise_reps,
        )
        return True


def delete_workout(request):
    exercise_id = request.GET.get('exercise_id')
    exercise = Exercise.objects.get(id=exercise_id)
    exercise.delete()
    return True


def get_workout_data(request):

    user_id = request.session.get('user_id')
    date = request.GET.get('date')

    exercises = Exercise.objects.filter(
        user_id=user_id,
        log_date=date
    ).select_related(
        'cardio_details',
        'weight_lifting_details'
    )

    workout_data_list = []
    total_duration_minutes = 0
    total_kcal_burn = 0

    for exercise in exercises:
        workout_entry = {
            'id': exercise.id,
            'log_date': exercise.log_date,
            'exercise_type': exercise.exercise_type,
            'exercise_name': exercise.exercise_name,
            'intensity': exercise.intensity,
            'kcal': exercise.kcal,
        }

        if exercise.exercise_type == 'Cardio' and hasattr(exercise, 'cardio_details'):
            workout_entry['cardio_details__duration_minutes'] = exercise.cardio_details.duration_minutes
            workout_entry['cardio_details__distance_km'] = exercise.cardio_details.distance_km
            total_duration_minutes += exercise.cardio_details.duration_minutes or 0
        else:
            workout_entry['cardio_details__duration_minutes'] = None
            workout_entry['cardio_details__distance_km'] = None

        if exercise.exercise_type == 'Weight Lifting' and hasattr(exercise, 'weight_lifting_details'):
            workout_entry['weight_lifting_details__sets'] = exercise.weight_lifting_details.sets
            workout_entry['weight_lifting_details__reps'] = exercise.weight_lifting_details.reps
            workout_entry['weight_lifting_details__weight_kg'] = exercise.weight_lifting_details.weight_kg
        else:
            workout_entry['weight_lifting_details__sets'] = None
            workout_entry['weight_lifting_details__reps'] = None
            workout_entry['weight_lifting_details__weight_kg'] = None

        total_kcal_burn += exercise.kcal or 0
        workout_data_list.append(workout_entry)


    header_data = {
        'cardio_details__duration_minutes__sum': total_duration_minutes,
        'kcal__sum': total_kcal_burn,
    }

    return workout_data_list, header_data
