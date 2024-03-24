from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Devices_details,Data_store,Admin_details
import time
from django.core.serializers import serialize
from datetime import timedelta, date
from django.db.models import Max
from datetime import datetime
from joblib import load
from django.http import JsonResponse
from datetime import time as dt_time
from .Commons import *

current_date_time_datetime = datetime.now()
graphdate=timezone.localdate()
totaldate=timezone.localdate()
todays=timezone.localdate()

model=load('./TheModel/model.joblib')
sessions=0

def home(request):
    global sessions
    if sessions==0:
        if 'load' in request.session:
            del request.session['load']
        sessions=1
    if 'admin' in request.session:
        del request.session['admin']
    if 'load' in request.session:
        loader="1"
    else:
        request.session['load'] = 1
        loader="0"
    datevalue = totaldate.strftime('%Y-%m-%d')
    return render(request, 'index.html',{'tdate':datevalue,'Load':loader})


def viewmoredetails(request):
    devices_data = Devices_details.objects.filter(device_id__in=[3,5,8]).values()
    return render(request,'details.html',{'Devices':devices_data})

def loadernew(request):
    global sessions
    sessions=0
    return JsonResponse({'status': 'success'})



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
    Did = request.GET.get('Device_id', None)
    if dayorweek==1:
        output=grweekdata(current_date,Did)
    else:
        output=grdaydata(current_date,Did)
    return JsonResponse( output,safe=False)


def livedatasend(request):
    device_limits=device_limitsdata()
    newdate = request.GET.get('devdates', None)
    current_date= datetime.strptime(newdate, "%Y-%m-%d").date()
    distinct_devices = Devices_details.objects.values('device_id').distinct()
    result = []
    for device in distinct_devices:
        barbottom="5px solid rgb(194, 194, 194)"
        barrigth="5px solid rgb(194, 194, 194)"
        barclass="low"
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
                        barclass="high"
                    color=device_limits['limits'][device_id]['HighColor']
                elif latest_record.device_values >=mid:
                    if device_id==6 or device_id==8:
                        barclass="mid"
                    color=device_limits['limits'][device_id]['MtoHColor']
                elif latest_record.device_values >=low:
                    if device_id==8:
                        barclass="mid"
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
                'barclass':barclass
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
                'barclass':barclass
            })
    result.sort(key=lambda x: x['device_id'])
    return JsonResponse(result,safe=False)


def grweekdata(current_date,did):
    symbols_data=icon_get()
    device_names=device_names_get()
    dates = []
    device2 = []
    device5 = []
    deviceid=int(did)
    if deviceid!=11:
        symbol=symbols_data[deviceid]
    else:
        symbol=""
    device_name=device_names[deviceid]
    for i in range(6, -1, -1):
        day = current_date - timedelta(days=i)
        dates.append(day)
        sql1 = Data_store.objects.filter(device_id=did, date_time__date=day).order_by('-date_time').first()
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
    output = [{'date': dates, 'value1': device2, 'value2': ra,'Names':device_name,'Symbols':symbol} for dates, device2, ra in zip(dates, device2, ra)]
    return output


def grdaydata(current_date,did):
    symbols_data=icon_get()
    device_names=device_names_get()
    device2 = []
    device5 = []
    deviceid=int(did)
    if deviceid!=11:
        symbol=symbols_data[deviceid]
    else:
        symbol=""
    device_name=device_names[deviceid]
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
        device_id=did,
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
    output = [{'date': times, 'value1': device2, 'value2': ra,'Names':device_name,'Symbols':symbol} for times, device2, ra in zip(times, device2, ra)]
    return output

def insertvalues(request):
    dataarray=[None]*11
    dataarray[0]=int(request.GET.get('hum', None))              # Humidity
    dataarray[1]=int(request.GET.get('temp', None))             # Temperature
    dataarray[2]=int(request.GET.get('sou', None))              # Sound
    dataarray[3]=int(request.GET.get('carbon', None))           # Co2
    dataarray[4]=0                                              # Chance of Rain
    dataarray[5]=int(request.GET.get('windspeed', None))        # Wind Speed
    dataarray[6]=int(request.GET.get('no2', None))              # NO2
    dataarray[7]=int(request.GET.get('press', None))            # Atmospheric Pressure
    dataarray[8]=int(request.GET.get('uv', None))               # UV
    dataarray[9]=152                                            # Wind Direction
    dataarray[10]=int(request.GET.get('pm25', None))            # Air Quality
    i=1
    for value in dataarray:
        insert_data = Data_store(device_values=value, device_id=i)
        insert_data.save()
        i+=1

    return JsonResponse("DONE",safe=False) 


