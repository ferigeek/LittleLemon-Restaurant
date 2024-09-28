from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', {'page_title': 'Home', 'host': request.get_host()})
