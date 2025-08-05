from django.urls import path
from . import views


app_name = 'reminder'

urlpatterns = [

    path('load_reminder_page', views.load_reminder_page,name='load_reminder_page'),
    path('api/reminder/', views.ReminderView.as_view(), name='reminder'),
    path('api/get_reminder/', views.ReminderView.as_view(), name='get_reminder'),
    path('api/delete_reminder/<int:pk>', views.ReminderView.as_view(), name='delete_reminder'),
    path('api/update_reminder/<int:pk>', views.ReminderView.as_view(), name='update_reminder'),

]