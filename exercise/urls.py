from django.urls import path
from . import views


app_name = 'exercise'

urlpatterns = [

    path('load_workout_page', views.load_workout_page,name='load_workout_page'),
    path('add_workout', views.add_workout,name='add_workout'),
    path('delete_workout', views.delete_workout,name='delete_workout'),
    path('api/get_data_based_on_date/', views.get_data_based_on_date, name='get_data_based_on_date'),
]