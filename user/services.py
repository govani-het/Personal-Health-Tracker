import random

from django.http import JsonResponse

from . import exception
import smtplib
from .models import UserData, ProfileSetUp
import bcrypt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def create_user(email, password):
    email = email.lower()
    if UserData.objects.filter(email=email).exists():
        raise ValueError("Email already registered")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

        user = UserData(email=email, password=hashed_password)
        user.save()


def authenticate_user(email, password):
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


def profile_setup(user_id, username, height, weight, goal, dob, gender, activity_level):
    global users_id
    users_id = user_id

    if ProfileSetUp.objects.filter(user_id=user_id).exists():
        raise exception.ProfileSetUpAlreadyExists("This Profile Setup Already Exists")
    else:
        user_data = UserData.objects.get(user_id=user_id)

        profile = ProfileSetUp(user_id=user_data, username=username, height=height, weight=weight, goal=goal, dob=dob,
                               gender=gender, activity_level=activity_level)

        profile.save()


def dashboard(user_id):
    user_profiles = ProfileSetUp.objects.filter(user_id=user_id).first()

    if user_profiles:
        weight = user_profiles.weight
        height = int(user_profiles.height) / 100
        goal = user_profiles.goal

        diff = goal - weight
        bmi = weight / (height * height)

        return diff, bmi


def send_otp(request, email,user_id):
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


def update_password(request,password):
    user_id = request.session['user_id']
    email = request.session['email']
    password = password

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

    user = UserData(user_id=user_id,email=email,password=hashed_password)
    user.save()
    request.session.flush()
    return JsonResponse({'status': 'success'})
