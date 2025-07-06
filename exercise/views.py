from django.shortcuts import render


def load_workout_page(request):
    return render(request,'exercise_page.html')