from django.urls import path
from . import views


app_name = 'nutrition'

urlpatterns = [

    path('load_nutrition_page', views.load_nutrition_page, name='load_nutrition_page'),
    path('add_meal', views.add_meal, name='add_meal'),
    path('delete_meal_date', views.delete_meal_data, name='delete_meal_data'),

]