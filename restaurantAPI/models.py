from django.db import models

# Create your models here.

class Booking(models.Model):
    Name = models.CharField(max_length=255)
    No_of_guests = models.IntegerField()
    BookingDate = models.DateTimeField()

    def __str__(self) -> str:
        return self.Name 

class Menu(models.Model):
    Title = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Inventory = models.BooleanField()
    Image = models.ImageField(upload_to='menu/', default='menu/Default.png')

    def __str__(self) -> str:
        return self.Title