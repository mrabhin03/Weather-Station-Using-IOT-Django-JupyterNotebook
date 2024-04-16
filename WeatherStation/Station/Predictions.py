from .models import Data_store
from datetime import timedelta
import numpy as np
import pandas as pd
from joblib import load
from django.http import JsonResponse

Temperature_Model=load('./TheModel/Temperature_Model.joblib')
Humidity_Model=load('./TheModel/Humidity_Ke_model.joblib')
Pressure_Model=load('./TheModel/Pressure_model.joblib')
WindSpeed_Model=load('./TheModel/WindSpeed_model.joblib')

Rain_model=load('./TheModel/Rain_Prediction.joblib')

def daygraphpred(current_date,start_time,end_time,did):
    predataset=[]
    did=int(did)
    lastdata= Data_store.objects.filter(device_id=did,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
    lastinput_value=lastdata.device_values if lastdata else 25
    for i in range(7, 0, -1):
        day = current_date - timedelta(days=i)
        olddatasql = Data_store.objects.filter(
        device_id=did,
        date_time__date=day,
        date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        olddata = olddatasql.device_values if olddatasql else lastinput_value
        predataset.append(olddata)
    predataset_format = np.array([predataset])
    
    if did==2:
        predicted_value = Temperature_Model.predict(predataset_format.reshape(1, 7))
    else:
        predicted_value = Humidity_Model.predict(predataset_format.reshape(1, 7))
    pred=int(predicted_value)
    return pred


def daygraphrainpred(current_date,start_time,end_time):
    humidity_data=[]
    wind_data=[]
    Pressure_data=[]
    temperature_data=[]
    uv_data=[]
    for i in range(7, 0, -1):
        day = current_date - timedelta(days=i)

        windsql = Data_store.objects.filter(device_id=6,
        date_time__date=day,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        windsp = windsql.device_values if windsql else 0
        wind_data.append(windsp)

        humiditysql = Data_store.objects.filter(device_id=1,
        date_time__date=day,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        humiditys = humiditysql.device_values if humiditysql else 0
        humidity_data.append(humiditys)

        Pressuresql = Data_store.objects.filter(device_id=8,
        date_time__date=day,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        Pressure = Pressuresql.device_values if Pressuresql else 0
        Pressure_data.append(Pressure)

        temperaturesql = Data_store.objects.filter(device_id=2,
        date_time__date=day,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        temperature = temperaturesql.device_values if temperaturesql else 0
        temperature_data.append(temperature)

        uvsql = Data_store.objects.filter(device_id=9,
        date_time__date=day,date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        uv = uvsql.device_values if uvsql else 0
        uv_data.append(uv)
    sample=[]
    wind_format = np.array([wind_data])
    sample.append(int(WindSpeed_Model.predict(wind_format.reshape(1, 7))))

    humidity_format = np.array([humidity_data])
    sample.append(int(Humidity_Model.predict(humidity_format.reshape(1, 7))))

    Pressure_format = np.array([Pressure_data])
    sample.append(int(Pressure_Model.predict(Pressure_format.reshape(1, 7))))

    temperature_format = np.array([temperature_data])
    sample.append(int(Temperature_Model.predict(temperature_format.reshape(1, 7))))

    columns = ['WindSpeed', 'Humidity', 'Pressure', 'Temperature']
    data = pd.DataFrame([sample], columns=columns)
    probability = Rain_model.predict_proba(data)
    chance=int(probability[0][2]*100)
    return chance



def weekend_prediction(device2,last):
    art=[]
    for yadata in device2:
        inval=yadata
        if yadata==0:
            filtered_arr = [x for x in device2 if x != 0]
            if not filtered_arr:
                filtered_arr.append(last)
            inval = min(filtered_arr)
        art.append(inval)
    new_data = np.array([art])
    predicted_temp = Temperature_Model.predict(new_data.reshape(1, 7))
    predata=int(predicted_temp)
    return predata


def rain_prediction(Windspeed,humidity,Pressure,temperature):
    input_values = []

    input_values.append(Windspeed)

    input_values.append(humidity)

    input_values.append(Pressure)

    input_values.append(temperature)


    columns = ['WindSpeed', 'Humidity', 'Pressure', 'Temperature']
    data = pd.DataFrame([input_values], columns=columns)
    probability = Rain_model.predict_proba(data)
    chance=round(probability[0][2]*100)
    return chance


def Todaystemppred(device_id):
    old_data_sql = Data_store.objects.filter(device_id=device_id).order_by('-date_time')[:7]
    device_values = [0,0,0,0,0,0,0]
    i=0
    for record in old_data_sql:
        device_values[i]=record.device_values
        i+=1
    device_values = device_values[::-1]

    predataset_format = np.array([device_values])
    predicted_value = Temperature_Model.predict(predataset_format.reshape(1, 7))
    predata=int(predicted_value) 
    return predata


def update_rain_database(request):
    rain_sql = Data_store.objects.filter(device_id=5).order_by('-id')
    for j in rain_sql:

        wind_sql=Data_store.objects.filter(device_id=6,date_time=j.date_time).first()
        WindSpeed=wind_sql.device_values

        Humidity_sql=Data_store.objects.filter(device_id=1,date_time=j.date_time).first()
        Humidity=Humidity_sql.device_values

        Pressure_sql=Data_store.objects.filter(device_id=8,date_time=j.date_time).first()
        Pressure=Pressure_sql.device_values

        Temperature_sql=Data_store.objects.filter(device_id=2,date_time=j.date_time).first()
        Temperature=Temperature_sql.device_values

        Rain_out=rain_prediction(WindSpeed,Humidity,Pressure,Temperature)

        update = Data_store.objects.get(id=j.id)
        update.device_values=Rain_out
        update.save()


    return JsonResponse("okay",safe=False)