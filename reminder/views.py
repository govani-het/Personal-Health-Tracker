from django.shortcuts import render

# Create your views here.
def load_reminder_page(request):
    return render(request,'reminder.html')