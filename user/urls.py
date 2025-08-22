from django.urls import path
from . import views,login_view


app_name = 'user'

urlpatterns = [

    path('', views.login, name='login_page'),
    path('index/', views.index, name='index'),
    path('check_profile_setup/', login_view.check_profile_setup, name='check_profile_setup'),
    path('register', views.register, name='register_page'),
    path('create_user', views.create_user, name='create_user'),
    path('authenticate_user', login_view.authenticate_user, name='login_page'),
    path('profile_setup', views.user_profile_setup, name='profile_setup'),
    path('progress_page', views.load_progress_page, name='progress_page'),
    path('load_settings', views.load_setting_page, name='load_setting_page'),
    path('logout_user', login_view.user_logout, name='user_logout'),

]