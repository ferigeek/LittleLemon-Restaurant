import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from restaurantAPI import forms

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        loggedIn = True
        return render(request, 'home.html', {
        'page_title': 'Home', 
        'host': f'{request.scheme}://{request.get_host()}',
        'loggedIn': loggedIn,
        'user_name': request.user.username,
    })
    
    loggedIn = False
    return render(request, 'home.html', {
        'page_title': 'Home', 
        'host': f'{request.scheme}://{request.get_host()}',
        'loggedIn': loggedIn,
    })

def booking(request):
    if not request.user.is_authenticated:
        return render(request, 'book.html', { 
        'page_title': 'Booking', 
        'host': f'{request.scheme}://{request.get_host()}',
        'loggedIn': False,
    })
    form = forms.BookingForm()
    alert = 0
    if request.method == 'POST':
        form = forms.BookingForm(request.POST)
        if form.is_valid():
            form.save()
            alert = 1
    return render(request, 'book.html', {
        'form': form, 
        'page_title': 'Booking', 
        'host': f'{request.scheme}://{request.get_host()}',
        'alert': alert,
        'loggedIn': True,
        'user_name': request.user.username,
    })

def menu(request):
    loggedIn = False
    if request.user.is_authenticated:
        loggedIn = True
    menu = requests.get(f'{request.scheme}://{request.get_host()}/api/menu')
    if menu.status_code == 200:
        data = menu.json()
        return render(request, 'menu.html', {
        'page_title': 'Menu',
        'host': f'{request.scheme}://{request.get_host()}',
        'menu_items': data,
        'loggedIn': loggedIn,
        'user_name': request.user.username,
    })
    else:
        data = {}
        return render(request, 'menu.html', {
            'page_title': 'Menu',
            'host': f'{request.scheme}://{request.get_host()}',
            'menu_items': data,
        })
    
def signUp(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.groups.add(Group.objects.get(name='Regular User'))
            return redirect('login')
    return render(request, 'sign-up.html', {
        'form': form, 
        'page_title': 'Sign up', 
        'host': f'{request.scheme}://{request.get_host()}',
        'loggedIn': False,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {
        'form': form, 
        'page_title': 'Login', 
        'host': f'{request.scheme}://{request.get_host()}',
        'loggedIn': False,
    })

def logout_view(request):
    logout(request)
    return redirect('home')