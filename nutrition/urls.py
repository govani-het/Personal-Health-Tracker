from django.urls import path
from . import views


app_name = 'nutrition'

urlpatterns = [

    path('load_nutrition_page', views.load_nutrition_page, name='load_nutrition_page'),

]