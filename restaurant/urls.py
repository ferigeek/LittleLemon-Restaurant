from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('home/', views.home, name='home'),
    path('book/', views.booking, name='booking'),
    path('menu/', views.menu, name='menu'),
    path('sign-up/', views.signUp, name='sign-up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
