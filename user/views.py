from django.shortcuts import render,redirect
from . import services
from .models import ProfileSetUp
from django.contrib import messages

def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')

def index(request):
    user_id = request.GET.get('user_id')
    print(user_id)
    dashboard = services.dashboard(user_id)
    return render(request, 'index.html',context={'dashboard':dashboard})

def load_progress_page(request):
    return render(request,'progress_page.html')

def load_setting_page(request):
    return render(request,'setting.html')

def create_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        try:
            services.create_user(email, password)
            return redirect('/')
        except ValueError as e:
            messages.error(request, str(e))

            return redirect('/register')
    else:
        return redirect('/register')

def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = services.authenticate_user(email, password)
            request.session['user_id'] = user.user_id

            if ProfileSetUp.objects.filter(user_id=user.user_id).exists():
                return redirect('/index?user_id='+str(user.user_id))
            else:
                return render(request, 'profile_setup.html')
        except services.exception.AuthenticationError as e:
            messages.error(request, str(e))
            return redirect('/')
        except services.exception.UserBlocked as e:
            messages.error(request, str(e))
            return redirect('/')

def user_profile_setup(request):

    if request.method == 'POST':
        user_id = request.session['user_id']
        username = request.POST['username']
        height = request.POST['height']
        weight = request.POST['weight']
        goal = request.POST['goal']
        dob = request.POST['dob']
        gender = request.POST['gender']
        activity_level = request.POST['activity_level']

        try:
            services.profile_setup(user_id, username, height, weight, goal, dob, gender, activity_level)
            return render(request, 'index.html')
        except services.exception.ProfileSetUpAlreadyExists as e:
            return render(request, 'index.html')
