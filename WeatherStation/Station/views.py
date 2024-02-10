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
        'limits': [{ #0 default
            'High': 20,
            'Mid': 10,
            'Low': 5
        },
        {
            #1 Humidity Sensor
            'HighColor':"red",
            'High': 60,
            'MtoHColor':"orange",
            'Mid': 30,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 15,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #2 Temperature Sensor
            'HighColor':"red",
            'High': 60,
            'MtoHColor':"orange",
            'Mid': 30,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 15,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #3 Sound Sensor
            'HighColor':"red",
            'High': 60, 
            'MtoHColor':"orange",
            'Mid': 30,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 15,
            'LowColor':"rgb(3, 209, 255)"
        },{
            #4 Co2 Sensor
            'HighColor':"rgb(255, 53, 53)",
            'High': 20, 
            'MtoHColor':"orange",
            'Mid': 5,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 2,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #5 Chance of Rain
            'HighColor':"rgb(0, 255, 174)",
            'High': 75, 
            'MtoHColor':"orange",
            'Mid': 50,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 30,
            'LowColor':"yellow"
        },
        {
            #6 Wind Speed sensor
            'HighColor':"red",
            'High': 25, 
            'MtoHColor':"orange",
            'Mid': 12,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 5,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #7 NO2 Sensor
            'HighColor':"red",
            'High': 20, 
            'MtoHColor':"orange",
            'Mid': 10,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 5,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #8 Atmospheric Pressure
            'HighColor':"red",
            'High': 1013, 
            'MtoHColor':"orange",
            'Mid': 980,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 550,
            'LowColor':"rgb(3, 209, 255)"
        },{
            #9 UV Sensor
            'HighColor':"red",
            'High': 40, 
            'MtoHColor':"orange",
            'Mid': 20,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 10,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #10 Wind Direction
            'HighColor':"red",
            'High': 10000, 
            'MtoHColor':"orange",
            'Mid': 10000,
            'LtoMColor':"rgb(81, 159, 226)",
            'Low': 10000,
            'LowColor':"rgb(3, 209, 255)"
        },
        {
            #11 Air Quality
            'HighColor':"red",
            'High': 30, 
            'MtoHColor':"orange",
            'Mid': 20,
            'LtoMColor':"rgb(0, 255, 174)",
            'Low': 15,
            'LowColor':"rgb(3, 209, 255)"
        }
    ]
}
device_icon = ["","cloudy-outline","thermometer-outline","volume-high-outline","warning-outline","umbrella-outline","speedometer-outline","logo-electron","contract-outline","warning-outline","compass-outline","balloon"]

def home(request):
    datevalue = totaldate.strftime('%Y-%m-%d')
    return render(request, 'Station/templates/index.html',{'tdate':datevalue})


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

def alldeviceonlydata(request):
    dates1=request.GET.get('grdates', None)
    current_date=datetime.strptime(dates1, "%Y-%m-%d").date()
    all_id = Devices_details.objects.aggregate(Max('device_id'))['device_id__max']
    dates=[]
    dayorweek = int(request.GET.get('dorw', None))
    if dayorweek==1:
        output=alldeviceonlydataweek(current_date,all_id,dates)
    else:
        output=alldeviceonlydataday(current_date,all_id,dates)
    
    
    return JsonResponse( output,safe=False)

def alldeviceonlydataday(current_date,all_id,dates):
    devices = [[] for _ in range(11)]
    times=[3,6,9,12,15,18,21,24]
    t=1
    for j in range(1, all_id + 1):
        devices_data = Devices_details.objects.filter(device_id__exact=j).values('device_id').first()
        device_id=devices_data['device_id']
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
            value1 = int(sql1.device_values if sql1 else 0)
            devices[j - 1].append(value1)
    output = [{'date': time, **{'Device{}'.format(i + 1): devices[i][j] for i in range(len(devices))}} for j, time in enumerate(times)]
    return output





def device_only_day(current_date,device_id,High,mid,low):
    device=[]
    icon=[]
    icon_data = device_icon[device_id]
    if device_id==2 or device_id==10:
        symbol="°"
    elif device_id==8:
        symbol="hPa"
    elif device_id==6:
        symbol="km/h"
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


def alldeviceonlydataweek(current_date,all_id,dates):
    devices = [[] for _ in range(11)]
    t=1
    for j in range(1, all_id + 1):
        devices_data = Devices_details.objects.filter(device_id__exact=j).values('device_id').first()
        device_id=devices_data['device_id']
        for i in range(6, -1, -1):
            day = current_date - timedelta(days=i)
            if t==1:
                dates.append(day)
            sql1 = Data_store.objects.filter(device_id=device_id, date_time__date=day).order_by('-date_time').first()
            value1 = int(sql1.device_values if sql1 else 0)
            devices[j - 1].append(value1)
        t=0
    output = [{'date': date, **{'Device{}'.format(i + 1): devices[i][j] for i in range(len(devices))}} for j, date in enumerate(dates)]
    return output





def device_only_week(current_date,device_id,High,mid,low):
    dates=[]
    device=[]
    icon=[]
    icon_data = device_icon[device_id]
    if device_id==2 or device_id==10:
        symbol="°"
    elif device_id==8:
        symbol="hPa"
    elif device_id==6:
        symbol="km/h"
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
        barbottom="5px solid rgb(194, 194, 194)"
        barrigth="5px solid rgb(194, 194, 194)"
        iconco="white"
        iconbg="rgb(81, 159, 226)"
        icon="sunny-outline"
        device_id = device['device_id']
        color="rgb(81, 159, 226)"
        latest_record = Data_store.objects.filter(
            device_id=device_id,
            date_time__date=current_date
        ).order_by('-date_time').first()

        if latest_record:
            High=device_limits['limits'][device_id]['High']
            mid=device_limits['limits'][device_id]['Mid']
            low=device_limits['limits'][device_id]['Low']
            if device_id==5:
                if latest_record.device_values>50:
                    color=device_limits['limits'][device_id]['HighColor']
                    iconco="black"
                elif latest_record.device_values<50:
                    color=color=device_limits['limits'][device_id]['LowColor']
                    iconco="black"
                else:
                    color=color=device_limits['limits'][device_id]['LtoMColor']
                    iconco="white"
                if latest_record.device_values>=75:
                    icon="rainy-outline"
                elif latest_record.device_values>=50:
                    icon="cloudy-outline"
                elif latest_record.device_values>=30:
                    icon="partly-sunny-outline"
                else:
                    icon="sunny-outline"
            elif device_id==3:
                if latest_record.device_values >=High:
                    color=device_limits['limits'][device_id]['HighColor']
                elif latest_record.device_values >=mid:
                    color=device_limits['limits'][device_id]['MtoHColor']
                elif latest_record.device_values >=low:
                    color=device_limits['limits'][device_id]['LtoMColor']
                else:
                    color=device_limits['limits'][device_id]['LowColor']

            else:
                if latest_record.device_values >=High:
                    if device_id==4:
                        iconbg="red"
                    if device_id==6 or device_id==8:
                        barbottom="5px solid rgb(6, 116, 212)"
                        barrigth="5px solid rgb(6, 116, 212)"
                    color=device_limits['limits'][device_id]['HighColor']
                elif latest_record.device_values >=mid:
                    if device_id==6 or device_id==8:
                        barbottom="5px solid rgb(6, 116, 212)"
                    color=device_limits['limits'][device_id]['MtoHColor']
                elif latest_record.device_values >=low:
                    if device_id==8:
                        barbottom="5px solid rgb(6, 116, 212)"
                    color=device_limits['limits'][device_id]['LtoMColor']
                else:
                    if device_id==4:
                        iconbg="violet"
                    color=device_limits['limits'][device_id]['LowColor']

            result.append({
                'device_id': latest_record.device_id,
                'date_time': latest_record.date_time,
                'device_values': latest_record.device_values,
                'Dev_Color':color,
                'Icon_color':iconco,
                'Icon':icon,
                'bgicon':iconbg,
                'barbottom':barbottom,
                'barrigth':barrigth
                
            })
        else:
            result.append({
                'device_id': device_id,
                'date_time': None,
                'device_values': 0,
                'Dev_Color':color,
                'Icon_color':iconco,
                'Icon':icon,
                'bgicon':iconbg,
                'barbottom':barbottom,
                'barrigth':barrigth
                
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