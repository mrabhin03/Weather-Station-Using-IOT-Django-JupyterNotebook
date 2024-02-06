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
from datetime import time as dt_time
current_date_time_datetime = datetime.now()

graphdate=timezone.localdate()
totaldate=timezone.localdate()

device_limits = {
        'limits': [{
            'High': 20,
            'Mid': 10,
            'Low': 5
        },
        {
            'High': 30,
            'Mid': 20,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 50,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 250,
            'Low': 15
        },{
            'High': 20,
            'Mid': 10,
            'Low': 5
        },
        {
            'High': 30,
            'Mid': 20,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 50,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 250,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 250,
            'Low': 15
        },{
            'High': 20,
            'Mid': 10,
            'Low': 5
        },
        {
            'High': 30,
            'Mid': 20,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 50,
            'Low': 15
        },
        {
            'High': 30,
            'Mid': 250,
            'Low': 15
        }
    ]
}
device_icon = ["","cloudy","thermometer","volume-high-outline","warning-outline","umbrella-outline","speedometer-outline","logo-electron","contract-outline","warning-outline","compass-outline","balloon"]

def home(request):
    k=1
    current_date=timeupdate(k)
    result=datacollection(current_date)
    bdata = {'weather_data': result}
    datevalue = totaldate.strftime('%Y-%m-%d')
    return render(request, 'Station/templates/index.html',{'database':bdata,'tdate':datevalue})


def viewmoredetails(request):
    devices_data = Devices_details.objects.values()
    return render(request,'Station/templates/details.html',{'Devices':devices_data})

def deviceonlydata(request):
    dates1=request.GET.get('grdates', None)
    current_date=datetime.strptime(dates1, "%Y-%m-%d").date()
    device_id = int(request.GET.get('theids', None))
    High=device_limits['limits'][device_id]['High']
    mid=device_limits['limits'][device_id]['Mid']
    low=device_limits['limits'][device_id]['Low']
    dayorweek = int(request.GET.get('dorw', None))
    if dayorweek==1:
        output=device_only_week(current_date,device_id,High,mid,low)
    else:
        output=device_only_day(current_date,device_id,High,mid,low)

    return JsonResponse( output,safe=False)

def device_only_day(current_date,device_id,High,mid,low):
    device=[]
    icon=[]
    icon_data = device_icon[device_id]
    if device_id==2 or device_id==6:
        symbol="°"
    else:
        symbol="%"
    times=[3,6,9,12,15,18,21,24]
    per=0
    tmin=0
    for time in times:
        hor=time
        if time==24:
            tmin=59
            hor=23
        
        start_time = dt_time(hour=per, minute=0)
        end_time = dt_time(hour=hor, minute=tmin)
        per=time
        sql1 = Data_store.objects.filter(
        device_id=device_id,
        date_time__date=current_date,
        date_time__time__range=(start_time, end_time)
        ).order_by('-date_time').first()
        value1 = sql1.device_values if sql1 else 0
        device.append(value1)
        if value1 >= High:
            icon.append("Red")
        elif value1 >= mid:
            icon.append("Orange")
        elif value1 >= low:
            icon.append("rgb(81, 159, 226)")
        else:
            icon.append("rgb(3, 209, 255)")
    output = [{'date': times, 'value': device, 'icons': icon_data,'color':icon,'symbol':symbol} for times, device,icon in zip(times, device,icon)]
    return output


def device_only_week(current_date,device_id,High,mid,low):
    dates=[]
    device=[]
    icon=[]
    icon_data = device_icon[device_id]
    if device_id==2 or device_id==6:
        symbol="°"
    else:
        symbol="%"
    for i in range(6, -1, -1):
        day = current_date - timedelta(days=i)
        dates.append(day)
        sql1 = Data_store.objects.filter(device_id=device_id, date_time__date=day).order_by('-date_time').first()
        value1 = int(sql1.device_values if sql1 else 0)
        device.append(value1)

        if value1 >= High:
            icon.append("Red")
        elif value1 >= mid:
            icon.append("Orange")
        elif value1 >= low:
            icon.append("rgb(81, 159, 226)")
        else:
            icon.append("rgb(3, 209, 255)")
    output = [{'date': dates, 'value': device, 'icons': icon_data,'color':icon,'symbol':symbol} for dates, device,icon in zip(dates, device,icon)]
    return output



def timeupdate(kr):
    if kr == 0:
        current_date = date(2024,5,5)
    else:
        current_date=timezone.localdate()
    return current_date

def valueup(request):
    dates1=request.GET.get('grdates', None)
    dateway = int(request.GET.get('way', None))
    dayorweek = int(request.GET.get('dorw', None))
    graphdate=datetime.strptime(dates1, "%Y-%m-%d").date()
    if dayorweek==1:
        if dateway==1:
            graphdate = graphdate - timedelta(days=7)
        else:
            graphdate = graphdate + timedelta(days=7)
    else:
        if dateway==1:
            graphdate = graphdate - timedelta(days=1)
        else:
            graphdate = graphdate + timedelta(days=1)
    return JsonResponse( graphdate,safe=False)


def day_update(request):
    global totaldate
    newdate = request.GET.get('dates', None)
    totaldate=datetime.strptime(newdate, '%Y-%m-%d')
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
    newdate = request.GET.get('grdates', None)
    dayorweek = int(request.GET.get('dorw', None))
    current_date= datetime.strptime(newdate, "%Y-%m-%d").date()
    if dayorweek==1:
        output=grweekdata(current_date)
    else:
        output=grdaydata(current_date)
    
    return JsonResponse( output,safe=False)


def livedatasend(request):
    newdate = request.GET.get('devdates', None)
    current_date= datetime.strptime(newdate, "%Y-%m-%d").date()
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




def grweekdata(current_date):
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
    return output

def grdaydata(current_date):
    device2 = []
    device5 = []
    times=[3,6,9,12,15,18,21,24]
    per=0
    tmin=0
    for time in times:
        hor=time
        if time==24:
            tmin=59
            hor=23
        
        start_time = dt_time(hour=per, minute=0)
        end_time = dt_time(hour=hor, minute=tmin)
        per=time
        sql1 = Data_store.objects.filter(
        device_id=2,
        date_time__date=current_date,
        date_time__time__range=(start_time, end_time)
        ).order_by('-date_time').first()
        value1 = sql1.device_values if sql1 else 0
        device2.append(value1)
        sql2 = Data_store.objects.filter(
        device_id=5,
        date_time__date=current_date,
        date_time__time__range=(start_time, end_time)
        ).order_by('-date_time').first()
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
    output = [{'date': times, 'value1': device2, 'value2': ra} for times, device2, ra in zip(times, device2, ra)]
    return output