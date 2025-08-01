import requests
from django.conf import settings
from .models import UserNutritionData
from user.models import UserData
from . import exception

NUTRITIONIX_API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"


def add_nutrition_data(user_id, meal_type, food_name):

    try:
        user_instance = UserData.objects.get(user_id=user_id)
    except:
        raise exception.UserNotFound(f"CRITICAL ERROR: User with id {user_id} does not exist in the database.")

    header = {
        'x-app-id': settings.NUTRITIONIX_APP_ID,
        'x-app-key': settings.NUTRITIONIX_API_KEY,
        'x-remote-user-id': str(user_id)
    }

    payload = {
        "query": food_name,
    }

    try:
        response = requests.post(NUTRITIONIX_API_URL, headers=header, json=payload)

        response.raise_for_status()

        nutrition_data = response.json()


        for data in nutrition_data.get('foods', []):
            UserNutritionData.objects.create(
                user_id=user_instance,
                meal_type=meal_type,
                food_quantity=data.get('serving_qty',1),
                food_name=data.get('food_name', 'N/A').title(),
                kcal=data.get('nf_calories', 0),
                protein=data.get('nf_protein', 0),
                carbs=data.get('nf_total_carbohydrate', 0),
                fats=data.get('nf_total_fat', 0),
            )


        return True

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        print(f"Error details from API: {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"A generic Request Error occurred: {e}")
        return False
    except exception.FoodNotFound:
        print(f"Food '{food_name}' does not exist in the database.")
        return False

def show_user_nutrition_data(user_id,date):
    try:
        user_nutrition_data = list(
            UserNutritionData.objects.filter(
                user_id=user_id,
                meal_date=date
            ).values(
                'id',
                'meal_type',
                'food_name',
                'food_quantity',
                'kcal',
                'protein',
                'carbs',
                'fats'
            )
        )
        return user_nutrition_data

    except exception.DataNotFound:
        print(f"Data Not Found For This Data: {date}")
        return False

def delete_nutrition_data(meal_id):
    user_nutrition_data = UserNutritionData.objects.filter(id=meal_id)
    if user_nutrition_data:
        user_nutrition_data.delete()
    return True

def count_nutrition_data(user_id,date):
    user_nutrition_data = UserNutritionData.objects.filter(user_id=user_id,meal_date=date)
    if user_nutrition_data:
        kcal = 0
        protein = 0
        carbs = 0
        fats = 0
        for data in user_nutrition_data:
            kcal += data.kcal
            protein += data.protein
            carbs += data.carbs
            fats += data.fats
        return kcal, protein, carbs, fats

def count_nutrition_data_by_percentage(user_id,date):
    user_nutrition_data = UserNutritionData.objects.filter(user_id=user_id,meal_date=date)
    if user_nutrition_data:
        kcal = 0
        protein = 0
        carbs = 0
        fats = 0
        for data in user_nutrition_data:
            kcal += data.kcal
            protein += data.protein
            carbs += data.carbs
            fats += data.fats

        kcal = int((kcal/2000)*100)
        protein = int((protein/150)*100)
        carbs = int((carbs/250)*100)
        fats = int((fats/70)*100)

        return kcal, protein, carbs, fats