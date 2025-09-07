from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import services
from user.login_view import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required()
def load_workout_page(request):
    return render(request, 'exercisePage.html', )


@login_required()
def add_workout(request):
    services.add_exercise(request)
    return redirect('exercise:load_workout_page')


@login_required()
def delete_workout(request):
    services.delete_workout(request)
    return redirect('exercise:load_workout_page')


@login_required()
def get_data_based_on_date(request):
    try:
        workout, header = services.get_workout_data(request)
        return JsonResponse(
            {'workout': workout, 'header': header}

        )
    except Exception as e:
        print(e)
        return render(request, 'exercisePage.html', {'Message': "Exercise Data Not Found"})
