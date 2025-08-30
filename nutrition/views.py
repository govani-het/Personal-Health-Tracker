from django.http import JsonResponse

from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from . import services
from . import exception
from user.login_view import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required()
def load_nutrition_page(request):
    user_id = request.session.get('user_id')
    date = datetime.now().strftime('%Y-%m-%d')
    if user_id is None:
        return redirect('/')
    try:
        nutrition_service = services.show_user_nutrition_data(user_id, date)
        count_nutrition = services.count_nutrition_data(user_id, date)
        total_nutrition = services.count_nutrition_data_by_percentage(user_id, date)

        return render(request, 'nutrition_page.html',
                      {'nutrition_service': nutrition_service, 'count_nutrition': count_nutrition,
                       'total_nutrition': total_nutrition})
    except exception.UserDataNotFound as e:
        messages.error(request, str(e))
        return render(request, 'nutrition_page.html', )


@login_required()
def add_meal(request):
    if request.method == "POST":

        user_id = request.session.get('user_id')
        meal_type = request.POST.get('meal_type')
        food_name = request.POST.get('food_name')

        try:
            services.add_nutrition_data(user_id, meal_type, food_name)
            return redirect('nutrition:load_nutrition_page')
        except Exception as e:

            messages.error(request, e)
            return redirect('nutrition:load_nutrition_page')


@login_required()
def delete_meal_data(request):
    meal_id = request.GET.get('meal_id')
    services.delete_nutrition_data(meal_id)
    return redirect('nutrition:load_nutrition_page')


@login_required()
def get_data_based_on_date(request):
    date = request.GET.get('date')
    user_id = request.session.get('user_id')

    if user_id is None:
        return redirect('/')

    if not date:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

    try:
        nutrition_data = services.show_user_nutrition_data(user_id, date)

        count_nutrition = services.count_nutrition_data(user_id, date)

        total_nutrition = services.count_nutrition_data_by_percentage(user_id, date)

        return JsonResponse({
            'meals': nutrition_data,
            'summary': count_nutrition,
            'percentages': total_nutrition
        })

    except Exception as e:

        print(f"An error occurred: {e}")

        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)
