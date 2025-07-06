from django.urls import path
from . import views


app_name = 'user'

urlpatterns = [

    path('', views.login, name='login_page'),
    path('index/', views.index, name='index'),
    path('register', views.register, name='register_page'),
    path('create_user', views.create_user, name='create_user'),
    path('authenticate_user', views.authenticate_user, name='login_page'),
    path('profile_setup', views.user_profile_setup, name='profile_setup'),
    path('progress_page', views.load_progress_page, name='progress_page'),
    path('load_settings', views.load_setting_page, name='load_setting_page'),

]