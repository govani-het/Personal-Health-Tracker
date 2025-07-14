import requests
from django.conf import settings
from .models import Exercise, Cardio, WeightLifting
from user.models import UserData
from . import exception

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"


def add_exercise(user_id, exercise_type, exercise_name, intensity, duration, distance, weight, exercise_set,
                 exercise_reps):
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
            user_id=user_instance,
            exercise_type=exercise_type,
            exercise_name=exercise_name,
            intensity=intensity,
            kcal=exercise_data['exercises'][0]['nf_calories']
        )
        Cardio.objects.create(
            exercise=new_exercise,
            duration=duration,
            distance=distance,
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
            user_id=user_instance,
            exercise_type=exercise_type,
            exercise_name=exercise_name,
            intensity=intensity,
            kcal=exercise_data['exercises'][0]['nf_calories']
        )
        WeightLifting.objects.create(
            exercise=new_exercise,
            weight=weight,
            exercise_set=exercise_set,
            exercise_reps=exercise_reps,
        )
        return True