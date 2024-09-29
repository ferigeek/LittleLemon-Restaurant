from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Menu
from .serializers import BookingSerializer, MenuSerializer

# Create your views here.

@api_view(['GET'])
def menu_items(request):
    menu = Menu.objects.all()
    serialized_menu = MenuSerializer(menu, many=True)
    return Response(serialized_menu.data)