from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    no_of_guests = models.IntegerField()
    booking_date = models.DateField(null=True)
    booking_time = models.TimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.user.first_name + ' ' + self.user.last_name

class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.BooleanField()
    image = models.ImageField(upload_to='menu/', default='menu/Default.png')

    def __str__(self) -> str:
        return self.title