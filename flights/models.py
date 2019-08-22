from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length = 3)
    city = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    # explanation of origin and destination modification
    # origin is going to be now referencing some other class(Airport in this case)
    # django models allows me to determine what happends when I delete an airport
    # for instance what models.CASCADE does is: if I delete an airport that has associated
    # to a corresponding origin, delete all the flights as well.
    # the related_name (departure) does is: If I have an airport and I want to access all of the flights
    # who origin is that airport I can use the name departure to be able to access to that

    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id} - {self.origin} to {self.destination}"

class Passenger (models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"