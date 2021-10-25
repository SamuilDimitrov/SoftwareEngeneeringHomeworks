from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from requests.api import request
from rest_framework.parsers import JSONParser

from cars.serializers import CarSerializer
from cars.models import Car
import requests

def index(request):
    return HttpResponse("Hello, world. I want to kill myself.")

def showCars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return JsonResponse(serializer.data, safe=False)

def timetable(request):
    url = "https://api-v3.mbta.com/predictions?page%5Boffset%5D=0&page%5Blimit%5D=10&sort=departure_time&include=schedule%2Cvehicle%2Ctrip&filter%5Bdirection_id%5D=0&filter%5Bstop%5D=place-north"
    raw_data = requests.get(url)
    try:
        raw_data = raw_data.json()
    except :
        return HttpResponse("Ops...")

    sorted_data = []

    for i in raw_data['data']:
        train_entry = {}

        schedule_id = i['relationships']['schedule']['data']['id']
        trip = next(item for item in raw_data['included'] if item["id"] == schedule_id)
        train_entry['departure_time'] = trip['attributes']['departure_time']

        trip_id = i['relationships']['trip']['data']['id']
        trip = next(item for item in raw_data['included'] if item["id"] == trip_id)
        train_entry['destination'] = trip['attributes']['headsign']

        if i['relationships']['vehicle']['data'] is None:
            train_entry['vehicle'] = "None"
        else:
            vehicle_id = i['relationships']['vehicle']['data']['id']
            trip = next(item for item in raw_data['included'] if item["id"] == vehicle_id)
            train_entry['vehicle'] = trip['attributes']['label']

        train_entry['track'] = "TBD" #нямам иидея от къде се взима това
        train_entry['status'] = i['attributes']['status']

        sorted_data.append(train_entry)

    return render(request, 'Homework2.html', {'data':sorted_data})