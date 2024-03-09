from django.http import JsonResponse
from datetime import datetime
from .models import Devices_details,Data_store,Admin_details
from django.db.models import Max
from datetime import time as dt_time
from datetime import timedelta, date
from .Commons import *

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


def deviceonlydata(request):
    dates1=request.GET.get('grdates', None)
    device_limits=device_limitsdata()
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
    device_icon=device_icon_name_get()
    icon_data = device_icon[device_id]
    symbols_data=icon_get()
    symbol=symbols_data[device_id]
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
    output = [{'date': times, 'value': device, 'icons': icon_data,'color':icon,'symbol':symbol,'ID':device_id} for times, device,icon in zip(times, device,icon)]
    return output





def device_only_week(current_date,device_id,High,mid,low):
    dates=[]
    device=[]
    icon=[]
    device_icon=device_icon_name_get()
    symbols_data=icon_get()
    icon_data = device_icon[device_id]
    symbol=symbols_data[device_id]
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
    output = [{'date': dates, 'value': device, 'icons': icon_data,'color':icon,'symbol':symbol,'ID':device_id} for dates, device,icon in zip(dates, device,icon)]
    return output

