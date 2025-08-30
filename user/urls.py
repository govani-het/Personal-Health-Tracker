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
    path('reset_password', login_view.reset_password, name='reset_password'),
    path('api/verify_email/',login_view.verify_email, name='verify_email'),
    path('forget_password', login_view.forget_password, name='forget_password'),
    path('api/check_otp/',login_view.check_otp,name='check_otp'),
    path('api/update_password/',login_view.update_password,name='update_password'),
    path('api/update_profile_data/', views.update_user_profile, name='update_profile_data'),
    path('api/change_password/', views.change_password, name='change_password'),

]