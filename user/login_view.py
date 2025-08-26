import json
from django.urls import reverse
from datetime import datetime, timedelta
from functools import wraps

from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from . import services
from .models import ProfileSetUp, UserData
from django.contrib import messages
import os
from dotenv import load_dotenv
import jwt
from djangoProject.settings import SECRET_KEY
from . import services


load_dotenv()
def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = services.authenticate_user(email, password)
            request.session['user_id'] = user.user_id
            if user:
                response = redirect('check_profile_setup/')

                response.set_cookie(os.getenv('ACCESSTOKEN'),value=jwt.encode({
                    'user_id': user.user_id,
                            'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXP')))
                },
                SECRET_KEY,
                os.getenv('HASH_ALGORITHM')),
                max_age=int(os.getenv('ACCESS_TOKEN_MAX_AGE'))//1000,
                httponly=True,
                secure=True)


                refresh = jwt.encode({
                    'user_id': user.user_id,
                    'exp' : datetime.utcnow() + timedelta(hours=int(os.getenv('REFRESH_TOKEN_EXP')))
                },SECRET_KEY,os.getenv('HASH_ALGORITHM'))

                response.set_cookie(os.getenv('REFRESHTOKEN'),value=refresh,max_age=int(os.getenv('REFRESH_TOKEN_MAX_AGE'))//1000,httponly=True,secure=True)

                return response
            else:
                return redirect('/')
        except services.exception.AuthenticationError as e:
            messages.error(request, str(e))
            return redirect('/')
        except services.exception.UserBlocked as e:
            messages.error(request, str(e))
            return redirect('/')


def check_profile_setup(request):
    user_id = request.session.get('user_id')
    if ProfileSetUp.objects.filter(user_id=user_id).exists():
        return redirect('/index')
    else:
        return render(request, 'profile_setup.html')


def login_required():
    def inner(fn):
        @wraps(fn)
        def decorator(request):

            try:
                access_token = request.COOKIES.get(os.getenv('ACCESSTOKEN'))
                if access_token is None:
                    return refresh_token(request,fn)

                else:
                    data = jwt.decode(access_token, SECRET_KEY, algorithms=['HS256'])

                    user_data = UserData.objects.filter(user_id=data['user_id'])
                    if user_data is not None:
                        user_list = [model_to_dict(i) for i in user_data]

                        if user_list[0]['active']== 1:
                            return fn(request)
                        else:
                            return redirect('/')

                    else:
                        error_message = 'Unauthorized Access'
                        messages.info(request, error_message)
                    return redirect('/')
            except Exception as ex:
                print("login_required route Exception>>>>", ex)
                return refresh_token(request, fn)

        return decorator

    return inner

def refresh_token(request, fn):
    try:
        refresh_token = request.COOKIES.get(os.getenv('REFRESHTOKEN'))
        if refresh_token is not None:

            data = jwt.decode(refresh_token, SECRET_KEY, algorithms=['HS256'])

            user_data = UserData.objects.filter(user_id=data['user_id'])
            if user_data is not None:
                response = fn(request)
                response.set_cookie(os.getenv("ACCESSTOKEN"),value=jwt.encode({
                    'user_id': data['user_id'],
                    'exp': datetime.utcnow() + timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXP')))
                },
                SECRET_KEY,os.getenv('HASH_ALGORITHM')),
                max_age=int(os.getenv('ACCESS_TOKEN_MAX_AGE')) // 1000,
                httponly=True,
                secure=True
                )

                refresh = jwt.encode({
                    'user_id': data['user_id'],
                    'exp': datetime.utcnow() + timedelta(hours=int(os.getenv('REFRESH_TOKEN_EXP')))
                }, SECRET_KEY, os.getenv('HASH_ALGORITHM'))

                response.set_cookie(os.getenv('REFRESHTOKEN'), value=refresh,
                                    max_age=int(os.getenv('REFRESH_TOKEN_MAX_AGE')) // 1000, httponly=True, secure=True)

                return response

        else:
            messages.error(request, 'Your Session Is Expired')
            return redirect('/')
    except Exception:
        return redirect('/')

def user_logout(request):

    response = redirect('/')
    response.set_cookie(os.getenv('ACCESSTOKEN'),max_age=int(os.getenv('TIME_OUT_MAX_AGE')))
    response.set_cookie(os.getenv('REFRESHTOKEN'),max_age=int(os.getenv('TIME_OUT_MAX_AGE')))

    return response



def reset_password(request):
    return render(request,'emailVerification.html')


# your_app/views.py

def verify_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'message': 'Email not provided.'}, status=400)

            user = UserData.objects.get(email=email)

            if user is not None:
                try:
                    services.send_otp(request,user.email,user.user_id)
                except Exception:
                    return JsonResponse({'message': 'Fails to send OTP'}, status=400)
            redirect_url = reverse('user:forget_password')
            return JsonResponse({
                'status': 'success',
                'message': 'User found. Redirecting...',
                'redirect_url': redirect_url
            })

        except UserData.DoesNotExist:

            return JsonResponse({'message': 'Email does not exist in our records.'}, status=404)

        except Exception as e:

            return JsonResponse({'message': 'An unexpected server error occurred.'}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
def forget_password(request):
    return render(request,'forgetPassword.html')

def check_otp(request):
    data = json.loads(request.body)
    otp = data.get('otp')
    session_otp = request.session.get('otp')

    if int(otp) == int(session_otp):
        return JsonResponse({'success': True, 'message': 'Your OTP has been verified.'})
    else:
        del request.session['otp']
        messages.error(request,'Your OTP is Wrong.')
        redirect_url = reverse('user:reset_password')
        return JsonResponse({'Error': True, 'redirect_url': redirect_url})

def update_password(request):
    try:
        data = json.loads(request.body)
        password = data.get('password')

        if password is not None:
            services.update_password(request,password)

            return JsonResponse({'success': True, 'message': 'Password updated.'})

    except Exception as e:
        return JsonResponse({'message': 'An unexpected server error occurred.'}, status=500)