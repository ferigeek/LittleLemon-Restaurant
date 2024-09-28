from django.shortcuts import render
from restaurantAPI import forms

# Create your views here.

def home(request):
    return render(request, 'home.html', {'page_title': 'Home', 'host': request.get_host()})

def booking(request):
    form = forms.BookingForm()
    alert = 0
    if request.method == 'POST':
        form = forms.BookingForm(request.POST)
        if form.is_valid():
            form.save()
            alert = 1
    return render(request, 'book.html', {'form': form, 'page_title': 'Booking', 'host': request.get_host(), 'alert': alert})