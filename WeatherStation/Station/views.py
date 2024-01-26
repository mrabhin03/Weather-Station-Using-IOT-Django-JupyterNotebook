from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import HttpResponse
from .models import Devices_details,Data_store
import time
from datetime import timedelta, date
from django.db.models import F, Max, Case, When, Value, IntegerField,Subquery, OuterRef,ExpressionWrapper,fields
from django.db.models.functions import Cast,TruncDate
from django.db.models import DateTimeField
from django.db.models.functions import Coalesce
from django.db.models import Subquery, OuterRef
from datetime import datetime
from django.http import JsonResponse

current_date_time_datetime = datetime.now()

graphdate=timezone.localdate()
totaldate=timezone.localdate()


def home(request):
    k=1
    current_date=timeupdate(k)
    result=datacollection(current_date)
    bdata = {'weather_data': result}
    datevalue = totaldate.strftime('%Y-%m-%d')
    return render(request, 'Station/templates/index.html',{'database':bdata,'tdate':datevalue})

def timeupdate(kr):
    if kr == 0:
        current_date = date(2024,5,5)
    else:
        current_date=timezone.localdate()
    return current_date

def valueup(request):
    global graphdate
    dateway = int(request.GET.get('way', None))
    if dateway==1:
        graphdate = graphdate - timedelta(days=7)
    else:
        graphdate = graphdate + timedelta(days=7)
    
    return JsonResponse( dateway,safe=False)


def day_update(request):
    global totaldate
    newdate = request.GET.get('dates', None)
    totaldate=newdate
    return JsonResponse( newdate,safe=False)

def today(request):
    dated = time.strftime("%d %b", time.localtime())
    timet = time.strftime("%H:%M", time.localtime())
    current_date = timezone.localdate()
    device_id=2
    result = []
    latest_record = Data_store.objects.filter(
        device_id=device_id,
            date_time__date=current_date
        ).order_by('-date_time').first()

    if latest_record:
        result.append({
                'device_id': latest_record.device_id,
                'date_time': latest_record.date_time,
                'device_values': latest_record.device_values
            })
    else:
        result.append({
                'device_id': device_id,
                'date_time': None,
                'device_values': 0
            })
    timeandall=str(result[0]['device_values'])+","+str(dated)+","+str(timet)
    return JsonResponse( timeandall,safe=False)


def datacollection(ar):
    current_date=ar
    distinct_devices = Devices_details.objects.values('device_id').distinct()

    result = []

    for device in distinct_devices:
        device_id = device['device_id']
        latest_record = Data_store.objects.filter(
            device_id=device_id,
            date_time__date=current_date
        ).order_by('-date_time').first()

        if latest_record:
            result.append({
                'device_id': latest_record.device_id,
                'date_time': latest_record.date_time,
                'device_values': latest_record.device_values
            })
        else:
            result.append({
                'device_id': device_id,
                'date_time': None,
                'device_values': 0
            })
    result.sort(key=lambda x: x['device_id'])
    return result




def gdatacal(request):
    current_date=graphdate
    dates = []
    device2 = []
    device5 = []
    for i in range(6, -1, -1):
        day = current_date - timedelta(days=i)
        dates.append(day)
        sql1 = Data_store.objects.filter(device_id=2, date_time__date=day).order_by('-date_time').first()
        value1 = sql1.device_values if sql1 else 0
        device2.append(value1)
        sql2 = Data_store.objects.filter(device_id=5, date_time__date=day).order_by('-date_time').first()
        value2 = sql2.device_values if sql2 else 0
        device5.append(value2)
    ra=[]
    for data in device5:
        data2_value = int(data)
        if data2_value >=75:
            rain="rainy-outline"
        elif data2_value >=50:
            rain="cloudy-outline"
        elif data2_value >=30:
            rain="partly-sunny-outline"
        else:
            rain="sunny-outline"
        ra.append(rain)
    output = [{'date': dates, 'value1': device2, 'value2': ra} for dates, device2, ra in zip(dates, device2, ra)]
    return JsonResponse( output,safe=False)


def livedatasend(request):
    current_date=totaldate
    distinct_devices = Devices_details.objects.values('device_id').distinct()

    result = []

    for device in distinct_devices:
        device_id = device['device_id']
        latest_record = Data_store.objects.filter(
            device_id=device_id,
            date_time__date=current_date
        ).order_by('-date_time').first()

        if latest_record:
            result.append({
                'device_id': latest_record.device_id,
                'date_time': latest_record.date_time,
                'device_values': latest_record.device_values
            })
        else:
            result.append({
                'device_id': device_id,
                'date_time': None,
                'device_values': 0
            })
    result.sort(key=lambda x: x['device_id'])
    return JsonResponse(result,safe=False)