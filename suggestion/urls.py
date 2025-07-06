from django.urls import path
from . import views


app_name = 'suggestion'

urlpatterns = [

    path('load_suggestion_page', views.load_suggestion_page,name='load_suggestion_page'),

]