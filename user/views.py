import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from . import services

from django.views.decorators.cache import never_cache
from django.contrib import messages
from user.login_view import login_required


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


@never_cache
@login_required()
def index(request):
    user_id = request.session.get('user_id')

    dashboard = services.dashboard(user_id)
    return render(request, 'index.html', context={'dashboard': dashboard})


@never_cache
@login_required()
def load_progress_page(request):
    try:
        progress_chart = services.progress_view(request)

        progress_chart_html = progress_chart.to_html(
            full_html=False,
            include_plotlyjs='cdn')

        context = {
            'progress_chart': mark_safe(progress_chart_html)
        }
        return render(request, 'progressPage.html', context)
    except Exception as e:
        messages.error('An error occured while loading the progress page.', e)
        return redirect('/index')

@never_cache
@login_required()
def load_setting_page(request):
    user_id = request.session.get('user_id')
    try:
        profile = services.get_profile(user_id)
        if profile:
            data = {
                'username': profile.username,
                'height': profile.height,
                'weight': profile.weight,
                'goal': profile.goal,
                'dob': profile.dob,
                'gender': profile.gender,
                'activity_level': profile.activity_level
            }
            return render(request, 'setting.html', data)
    except Exception as e:
        return render(request, 'setting.html', context={'error': 'Profile data not found'})

    return render(request, 'setting.html')


def create_user(request):
    if request.method == "POST":
        try:
            response = services.create_user(request)

            if response.get('success'):
                return redirect('/')
            else:
                messages.error(request, response.get('message'))
                return redirect('/register')
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('/register')
        except Exception as e:
            messages.error(request, "Something went wrong, Please try again.")
            return redirect('/register')
    else:
        return redirect('/register')


@never_cache
@login_required()
def user_profile_setup(request):
    if request.method == 'POST':
        try:
            services.profile_setup(request)
            return redirect('user:index')
        except services.exception.ProfileSetUpAlreadyExists as e:
            messages.error(request, "Profile setup already exists")
            return render(request, 'index.html')


@login_required()
def update_user_profile(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)

    user = request.session.get('user_id')
    result = services.update_profile(user, data)
    if result['success']:
        return JsonResponse(result, status=200)
    else:
        status_code = 404 if 'exist' in result.get('message', '') else 400
        return JsonResponse(result, status=status_code)


@login_required()
def change_password(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        try:
            data = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format in request body.'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Failed to process request body.'}, status=400)

        response = services.change_password(user_id, data)

        if response['success']:
            return JsonResponse(response, status=200)
        else:
            return JsonResponse(response, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)
