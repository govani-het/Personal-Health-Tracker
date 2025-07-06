from django.shortcuts import render

def load_nutrition_page(request):
    return render(request,'nutrition_page.html')
