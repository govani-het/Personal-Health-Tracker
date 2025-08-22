from . import exception

from .models import UserData, ProfileSetUp
import bcrypt


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
