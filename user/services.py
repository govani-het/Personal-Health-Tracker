import os
import random
from datetime import date, timedelta
from django.db.models import Sum

from django.http import JsonResponse
from django.core.cache import cache

from . import exception
import smtplib
from .models import UserData, ProfileSetUp
from exercise.models import Exercise
from nutrition.models import UserNutritionData

import plotly.graph_objects as go

import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


def create_user(request):
    email = request.POST['email']
    password = request.POST['password']
    email = email.lower()
    if UserData.objects.filter(email=email).exists():
        return {'success': False, 'message': 'Email already registered'}
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
        user = UserData(email=email, password=hashed_password)
        user.save()
        return {'success': True}

def authenticate_user(request):
    email = request.POST['email']
    password = request.POST['password']
    email = email.lower()

    if UserData.objects.filter(email=email).exists():
        user = UserData.objects.get(email=email)
        if user.active:
            hashed_password = UserData.objects.get(email=email).password

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user
            else:
                raise exception.AuthenticationError('Please enter a valid Username and Password')
        else:
            raise exception.UserBlocked('You are Currently Blocked By Web site')
    else:
        raise exception.AuthenticationError("Please enter a valid Username and Password")


def profile_setup(request):
    user_id = request.session['user_id']
    username = request.POST['username']
    height = request.POST['height']
    weight = request.POST['weight']
    goal = request.POST['goal']
    dob = request.POST['dob']
    gender = request.POST['gender']
    activity_level = request.POST['activity_level']

    if ProfileSetUp.objects.filter(user_id=user_id).exists():
        raise exception.ProfileSetUpAlreadyExists("This Profile Setup Already Exists")
    else:
        user_data = UserData.objects.get(user_id=user_id)

        profile = ProfileSetUp(user_id=user_data, username=username, height=height, weight=weight, goal=goal, dob=dob,
                               gender=gender, activity_level=activity_level)

        profile.save()


def update_profile(user_id, data):
    try:
        profile = ProfileSetUp.objects.get(user_id=user_id)

        profile.username = data.get('username')
        profile.height = data.get('height')
        profile.weight = data.get('weight')
        profile.goal = data.get('goal')
        profile.dob = data.get('dob')
        profile.gender = data.get('gender')
        profile.activity_level = data.get('activityLevel')

        profile.save()

        return {'success': True, 'message': 'Profile updated successfully!'}

    except ProfileSetUp.DoesNotExist:
        return {'success': False, 'message': 'Profile does not exist for this user.'}

    except Exception as e:
        return {'success': False, 'message': f'An unexpected error occurred: {str(e)}'}


def get_profile(user_id):
    try:
        profile = ProfileSetUp.objects.get(user_id=user_id)
        return profile
    except ProfileSetUp.DoesNotExist:
        return None


def dashboard(user_id):
    user_profiles = ProfileSetUp.objects.filter(user_id=user_id).first()

    if user_profiles:
        weight = user_profiles.weight
        height = int(user_profiles.height) / 100
        goal = user_profiles.goal

        remaining_weight = goal - weight
        bmi = weight / (height * height)

        return remaining_weight, bmi


def send_otp(request, email, user_id):
    request.session['user_id'] = user_id
    request.session['email'] = email
    password = os.getenv('EMAIL_PASSWORD')
    sender = os.getenv('EMAIL_USER')
    receiver = email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "OTP"
    otp = random.randint(100000, 999999)
    request.session['otp'] = otp
    msg.attach(MIMEText('Your OTP is: ' + str(otp), 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    text = msg.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()
    return JsonResponse({'status': 'success'})


def update_password(request, data):
    user_id = request.session['user_id']
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

    UserData.objects.filter(user_id=user_id).update(password=hashed_password)
    request.session.flush()
    return JsonResponse({'status': 'success'})


def change_password(user_id, data):
    try:
        current_password = data.get('password').strip()
        new_password = data.get('newPassword').strip()

        if not current_password or not new_password:
            return {'success': False, 'message': 'Missing password fields.'}

        if current_password == new_password:
            return {'success': False, 'message': 'New password cannot be the same as the current password.'}

        hash_password = UserData.objects.get(user_id=user_id).password

        if bcrypt.checkpw(current_password.encode('utf-8'), hash_password.encode('utf-8')):
            updated_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')
            UserData.objects.filter(user_id=user_id).update(password=updated_password)
            return {'success': True, 'message': 'Password updated successfully!'}
        else:
            return {'success': False, 'message': 'Current Password Is Wrong'}

    except UserData.DoesNotExist:
        return {'success': False, 'message': 'User not found.'}
    except Exception as e:
        print(e)
        return {'status': False, 'message': 'An unexpected error occurred'}


def line_chart(dates, burned_data, consumed_data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=burned_data, mode='lines+markers', name='Burned KCAL',
        line=dict(color='skyblue', width=3), marker=dict(size=8, color='steelblue')
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=consumed_data, mode='lines+markers', name='Consumed KCAL',
        line=dict(color='gray', dash='dash', width=2)
    ))

    fig.update_layout(
        title={'text': 'Burned & Consumed KCAL', 'font': {'size': 24, 'color': '#333'}, 'x': 0.5},
        xaxis={'title': 'Date'}, yaxis={'title': 'KCAL'}, hovermode='x unified',
        template='plotly_white', height=500, margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family='Arial', size=24, color='#7f7f7f'),
    )
    return fig


def progress_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None


    today = date.today()

    cache_key = f"charts:progress_view:{user_id}:{today.isoformat()}"

    charts = cache.get(cache_key)

    if charts is not None:
        return charts

    thirty_days_ago = today - timedelta(days=29)

    exercise_entries = Exercise.objects.filter(
        user_id=user_id,
        log_date__gte=thirty_days_ago).values('log_date').annotate(total_kcal=Sum('kcal')).order_by('log_date')

    nutrition_entries = UserNutritionData.objects.filter(
        user_id=user_id,
        meal_date__gte=thirty_days_ago).values('meal_date').annotate(total_kcal=Sum('kcal')).order_by('meal_date')

    daily_burn_kcal_total = {entry['log_date']: entry['total_kcal'] for entry in exercise_entries}

    daily_consumed_kcal_total = {entry['meal_date']: entry['total_kcal'] for entry in nutrition_entries}

    all_dates_in_period = [thirty_days_ago + timedelta(days=i) for i in range(30)]

    burn_kcal_chart = [daily_burn_kcal_total.get(d, 0) for d in all_dates_in_period]

    consume_kcal_chart = [daily_consumed_kcal_total.get(d, 0) for d in all_dates_in_period]

    chart = line_chart(all_dates_in_period, burn_kcal_chart, consume_kcal_chart)

    cache.set(cache_key, chart,timeout=60*60*24)

    return chart
