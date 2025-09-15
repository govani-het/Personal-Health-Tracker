from django.urls import path
from . import views


app_name = 'nutrition'

urlpatterns = [

    path('load_nutrition_page', views.load_nutrition_page, name='load_nutrition_page'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('delete_meal_data', views.delete_meal_data, name='delete_meal_data'),
    path('api/get_data_based_on_date/', views.get_data_based_on_date, name='get_data_based_on_date'),

]