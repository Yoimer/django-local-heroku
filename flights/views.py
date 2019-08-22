from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# from this current models module - package
from .models import Flight, Passenger

# Create your views here.
def index(request):
    # return HttpResponse("Welcome to DjangoAir!")
    # render takes a couple of arguments, the request and the html template, context
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        # get rid of things that don't have this particular property
        # get rid of passengers who have this particular flight already in the list of flights
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "flights/flight.html", context)

def book(request, flight_id):
    try:
        # get passenger id
        passenger_id = int(request.POST["passenger"])
        # get passenger
        passenger = Passenger.objects.get(pk=passenger_id)
        # get passenger's flight
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request,  "flights/error.html", {"message": "No Selection."})
    except Flight.DoesNotExist:
        return render(request,  "flights/error.html", {"message": "No Flight."})
    except Passenger.DoesNotExist:
        return render(request,  "flights/error.html", {"message": "No passenger."})

    # adds passenger to that flight
    passenger.flights.add(flight)

    # the name of the route is flight (it is saved in url.py)
    # if you know the route of the url you want to go to, use reverse
    # the arguments of reverse are tuples of what arguments get passed into the flight
    return HttpResponseRedirect(reverse("flight", arg=(flight_id,)))