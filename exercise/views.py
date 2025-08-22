from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from . import services
from user.login_view import login_required


@login_required()
def load_workout_page(request):
    user_id = request.session.get('user_id')
    current_date = datetime.now().strftime('%Y-%m-%d')
    date = request.GET.get('date')

    if user_id is None:
        return redirect('')

    try:
        if date is None:
            workout = services.read_exercises_data(user_id, current_date)

            return render(request, 'exercise_page.html', {'workout': workout})
        else:
            workout = services.get_exercises_data(user_id, date)
            return render(request, 'exercise_page.html', {'workout': workout})
    except:
        return render(request, 'exercise_page.html', {'workout': None})

@login_required()
def add_workout(request):

    user_id = request.session.get('user_id')
    exercise_type = request.POST.get('exercise_type')
    exercise_name = request.POST.get('exercise_name')
    intensity = request.POST.get('intensity')


    if exercise_type == 'Cardio':
        duration = request.POST.get('duration')
        distance = request.POST.get('distance')
        services.add_exercise(user_id=user_id, exercise_type=exercise_type, exercise_name=exercise_name,
                              intensity=intensity, duration=duration, distance=distance, exercise_set=None,
                              exercise_reps=None, weight=None)

    if exercise_type == 'Weight Lifting':
        exercise_set = request.POST.get('sets')
        weight = request.POST.get('weight')
        exercise_reps = request.POST.get('reps')
        services.add_exercise(user_id=user_id, exercise_name=exercise_name, exercise_type=exercise_type,
                              intensity=intensity, exercise_set=exercise_set, weight=weight,
                              exercise_reps=exercise_reps, distance=None, duration=None)

    return redirect('exercise:load_workout_page')

@login_required()
def delete_workout(request):
    exercise_id = request.GET.get('exercise_id')

    services.delete_workout(exercise_id)
    return redirect('exercise:load_workout_page')

@login_required()
def get_data_based_on_date(request):

    user_id = request.session.get('user_id')
    date = request.GET.get('date')

    if user_id is None:
        return redirect('')
    try:
        workout = services.get_exercises_data(user_id, date)
        print(workout)
        return JsonResponse(
            {'workout': workout}
        )
    except:
        return render(request, 'exercise_page.html', {'workout': None})