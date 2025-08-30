import random

from django.http import JsonResponse

from . import exception
import smtplib
from .models import UserData, ProfileSetUp
import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_user(request):
    email = request.POST['email']
    password = request.POST['password']
    email = email.lower()
    if UserData.objects.filter(email=email).exists():
        raise ValueError("Email already registered")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

        user = UserData(email=email, password=hashed_password)
        user.save()


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

        diff = goal - weight
        bmi = weight / (height * height)

        return diff, bmi


def send_otp(request, email, user_id):
    request.session['user_id'] = user_id
    request.session['email'] = email
    password = "txjh gvgg jlfk hkcg"
    sender = "hetwww0@gmail.com"
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
        current_password = data.get('password')
        new_password = data.get('newPassword')

        if not current_password or not new_password:
            return {'success': False, 'message': 'Missing password fields.'}

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
        return {'status': 'failed', 'message': 'An unexpected error occurred'}
