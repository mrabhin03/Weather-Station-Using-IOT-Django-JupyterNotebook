from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import ev_data_store,Devices_details
import time
from datetime import datetime

current_date_time_datetime = datetime.now()

current_date_time_time = time.localtime()

dated = time.strftime("%d %b", time.localtime())
timet = time.strftime("%H:%M", time.localtime())



totaldata={
        'Humidity':50,
        'Temperature' : 30,
        'Sound' : 3,
        'co2' : 13,
        'Rain' : 1,
        }

def home(request):
    weather_data_queryset = ev_data_store.objects.filter(id=1)
    
    # Iterate through the queryset and print the data
    for weather_data_entry in weather_data_queryset:
        print(f"ID: {weather_data_entry.id}, Data: {weather_data_entry.data}, Time: {weather_data_entry.Time}")
    return render(request, 'MainBase/templates/index.html',{'tdata':totaldata,'ttime':timet,'tdate':dated})