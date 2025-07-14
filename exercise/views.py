from django.shortcuts import render, redirect
from . import services

def load_workout_page(request):
    return render(request,'exercise_page.html')


def add_workout(request):
    user_id = request.session.get('user_id')
    exercise_type = request.POST.get('exercise_type')
    exercise_name = request.POST.get('exercise_name')
    intensity = request.POST.get('intensity')

    if exercise_type == 'Cardio':

        duration = request.POST.get('duration')
        distance = request.POST.get('distance')
        response = services.add_exercise(user_id=user_id,exercise_type=exercise_type,exercise_name=exercise_name,intensity=intensity,duration=duration,distance=distance,exercise_set=None,exercise_reps=None,weight=None)

    if exercise_type == 'Weight Lifting':
        exercise_set = request.POST.get('sets')
        weight = request.POST.get('weight')
        exercise_reps = request.POST.get('reps')
        response = services.add_exercise(user_id=user_id, exercise_name=exercise_name, exercise_type=exercise_type, intensity=intensity, exercise_set=exercise_set, weight=weight, exercise_reps=exercise_reps,distance=None,duration=None)

    return redirect('exercise:load_workout_page')