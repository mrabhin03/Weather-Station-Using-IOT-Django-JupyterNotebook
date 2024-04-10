from django.shortcuts import render,redirect
from .models import Devices_details,Data_store
from django.utils import timezone
import calendar
from .Commons import *
from django.http import JsonResponse


todays=timezone.localdate()

def calender(request):
    month_y=str(todays.year)+"-"+str("{:02d}".format(todays.month))
    limit=range(7*6)
    days=["SUN","MON","TUE","WED","THR","FRI","SAT"]
    return render(request, 'calender.html',{'days':days,'limit':limit,'month_y':month_y})



def id_change(request):

    did = int(request.GET.get('id', None))
    date_data = request.GET.get('date_value', None)
    year, month = date_data.split("-")
    year=int(year)
    month=int(month)
    values_data=[]
    name=device_names_get()
    week_day=weekdays()
    symboles=icon_get()
    i=0
    thenoweek=calendar.weekday(year, month, 1)
    for j in range(thenoweek+1):
        i+=1
        values_data.append({
            'Date':0,
            'Value':0,
            'Symbole':"",
            'Name':name[did],
            'Today':""
        })
    
    num_days = calendar.monthrange(year, month)[1]
    data_sy=symboles[did]
    for day in range(1, num_days + 1):
        day_val="{year}-{month:02d}-{day:02d}".format(year=year, month=month, day=day)
        if day_val==str(todays):
            Tday="Today"
        else:
            Tday=""
        thedate="{day:02d}".format(day=day)
        sql1 = Data_store.objects.filter(device_id=did, date_time__date=day_val).order_by('-date_time').first()
        value1 = sql1.device_values if sql1 else "---"
        data_sy=symboles[did] if sql1 else ""
        values_data.append({
            'Date':thedate,
            'Value':value1,
            'Symbole':data_sy,
            'Name':name[did],
            'Today':Tday
            })
        i+=1
    while i!=42:
        values_data.append({
            'Date':0,
            'Value':0,
            'Symbole':"",
            'Name':name[did],
            'Today':""
        })
        i+=1
    return JsonResponse( values_data,safe=False)