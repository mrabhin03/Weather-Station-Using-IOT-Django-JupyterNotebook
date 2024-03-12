from django.http import JsonResponse
from django.utils import timezone
from .models import Devices_details,Data_store,Admin_details
from .Commons import *
from django.shortcuts import render,redirect
todays=timezone.localdate()


def admindata(request):
    if 'load' in request.session:
        del request.session['load']
    device_names=device_names_get()
    symbols_data=icon_get()
    device_icon=device_icon_name_get()
    data=[1,2,3,4,5,6,7,8,9]
    if 'admin' in request.session:
        current_date= todays
        distinct_devices = Devices_details.objects.values('device_id').distinct()
        Active = Devices_details.objects.filter(device_status=1).count()
        result = []
        count=0
        for device in distinct_devices:
            count+=1
            device_id = device['device_id']
            names_d=device_names[device_id]
            latest_record = Data_store.objects.filter(
                device_id=device_id
            ).order_by('-date_time').first()
            status=Devices_details.objects.filter(device_id=device_id).values('device_status','device_name','device_details').first()
            symbol=symbols_data[device_id]
            if latest_record:
                datetm = latest_record.date_time.date()
                timetm = latest_record.date_time.time()
                if current_date==datetm:
                    datetm="Today at "+timetm.strftime("%I:%M %p")
                else:
                    datetm=str(datetm)+" at "+timetm.strftime("%I:%M %p")
                result.append({
                    'device_id': latest_record.device_id,
                    'icon': device_icon[device_id],
                    'name':status['device_name'],
                    'date': datetm,
                    'details':status['device_details'],
                    'status':status['device_status']
                })
            else:
                result.append({
                    'device_id': device_id,
                    'icon': device_icon[device_id],
                    'name':status['device_name'],
                    'date':"No data",
                    'details':status['device_details'],
                    'status':status['device_status']
                })
        result.sort(key=lambda x: x['device_id'])
        return render(request,'admin_page.html',{'datat':result,'Total':count,'active':Active,'inactive':count-Active})
    else:
        return redirect('login')
        
def login(request):
    if request.method == 'POST':
        requsername=request.POST.get('username', None)
        reqpassword=request.POST.get('password', None)
        datauser=Admin_details.objects.filter(
        username=requsername).first()
        if datauser is not None:
            if reqpassword==datauser.password:
                request.session['admin'] = 1
                return redirect('admindata')
            else:
                return render(request, 'login.html', {'errormsg': "Wrong Password"})
        else:
            return render(request, 'login.html', {'errormsg': "User not found"})
            
    return render(request,'login.html',{'errormsg': ""})


def logout(request):
    if 'admin' in request.session:
        del request.session['admin']
    return redirect('home')


def dataview(request):
    return render(request,'admin_data.html')


def admin_lastdata(request):
    device_names=device_names_get()
    symbols_data=icon_get()
    result=[]
    device_id=int(request.GET.get('device_id',None))
    date=request.GET.get('dates',None)
    fulldata = Data_store.objects.filter(device_id=device_id, date_time__date=date).order_by('-date_time')
    symbol=symbols_data[device_id]
    names_d=device_names[device_id]
    if len(fulldata) == 0:
        result.append({
            'device_id': device_id,
            'datetime': "No data",
            'range': "404",
            'device_values': "No data"+str(symbol),
            'Name':names_d,
            'max':"--",
            'min':"--"})
    else:
        maxval = max(data.device_values for data in fulldata)
        minval = min(data.device_values for data in fulldata)
    for device in fulldata:
            timetm = device.date_time.time()
            timetm=timetm.strftime("%I:%M %p")
            if device_id!=10:
                range_data=therangecheck(device.device_values,device.device_id)
                values_data=str(device.device_values)+str(symbol)
                max_data=str(maxval)+str(symbol)
                min_data=str(minval)+str(symbol)
            else:
                range_datat=therangecheck(device.device_values,device.device_id)
                range_data=range_datat[0]['From']+" To "+range_datat[0]['To']
                values_data=str(device.device_values)+str(symbol)+range_datat[0]['To']
                max_symbol_data=therangecheck(maxval,device_id)
                max_data=str(maxval)+str(symbol)+max_symbol_data[0]['To']
                min_symbol_data=therangecheck(minval,device_id)
                min_data=str(minval)+str(symbol)+min_symbol_data[0]['To']
            result.append({
                'device_id': device.device_id,
                'datetime': timetm,
                'range': range_data,
                'device_values': values_data,
                'Name':names_d,
                'max':max_data,
                'min':min_data})
    return JsonResponse(result,safe=False)


def therangecheck(values,device_id):
    device_limits=device_limitsdata()
    winddirval=[]
    if device_id!=10:
        High=device_limits['limits'][device_id]['High']
        mid=device_limits['limits'][device_id]['Mid']
        low=device_limits['limits'][device_id]['Low']
        if values >=High:
            rangeval="Unhealthy"
        elif values >=mid:
            rangeval="Moderate"
        elif values >=low:
            rangeval="Good"
        else:
            rangeval="Low"
        return rangeval
    else:
        winddir=values
        if winddir == 0:
            winddirval.append({
                'From': 'S',
                'To': 'N',
                })
        elif winddir == 90:
            winddirval.append({
                'From': 'W',
                'To': 'E',
                })
        elif winddir == 180:
            winddirval.append({
                'From': 'N',
                'To': 'S',
                })
        elif winddir == 270:
            winddirval.append({
                'From': 'E',
                'To': 'W',
                })
        else:
            if winddir < 90:
                winddirval.append({
                'From': 'SW',
                'To': 'NE',
                })
            elif winddir < 180:
                winddirval.append({
                'From': 'SE',
                'To': 'NW',
                })
            elif winddir < 270:
                winddirval.append({
                'From': 'NE',
                'To': 'SW',
                })
            elif winddir < 360:
                winddirval.append({
                'From': 'NW',
                'To': 'SE',
                })
        return winddirval
    

def thestatuschange(request):
    id=request.GET.get("id")
    status=request.GET.get("status")
    obj = Devices_details.objects.filter(device_id=id).first()
    obj.device_status = status
    obj.save()
    return JsonResponse(0,safe=False)