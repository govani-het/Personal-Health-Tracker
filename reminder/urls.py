from django.urls import path
from . import views


app_name = 'reminder'

urlpatterns = [

    path('load_reminder_page', views.load_reminder_page,name='load_reminder_page'),

]