from django.shortcuts import render

# Create your views here.
def load_suggestion_page(request):
    return render(request,'suggestion.html')