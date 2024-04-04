from .models import Data_store
from datetime import timedelta
import numpy as np
import pandas as pd
from joblib import load
model=load('./TheModel/Temperature_Model.joblib')
Rain_model=load('./TheModel/Rain_Prediction.joblib')

def daygraphpred(current_date,start_time,end_time,did):
    predataset=[]
    for i in range(7, 0, -1):
        day = current_date - timedelta(days=i)
        olddatasql = Data_store.objects.filter(
        device_id=did,
        date_time__date=day,
        date_time__time__range=(start_time, end_time)).order_by('-date_time').first()
        olddata = olddatasql.device_values if olddatasql else 0
        predataset.append(olddata)
    predataset_format = np.array([predataset])
    predicted_value = model.predict(predataset_format.reshape(1, 7))
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
    sample.append(int(model.predict(wind_format.reshape(1, 7))))

    humidity_format = np.array([humidity_data])
    sample.append(int(model.predict(humidity_format.reshape(1, 7))))

    Pressure_format = np.array([Pressure_data])
    sample.append(int(model.predict(Pressure_format.reshape(1, 7))))

    temperature_format = np.array([temperature_data])
    sample.append(int(model.predict(temperature_format.reshape(1, 7))))

    uv_format = np.array([uv_data])
    sample.append(int(model.predict(uv_format.reshape(1, 7))))

    columns = ['WindSpeed', 'Humidity', 'Pressure', 'Temperature','UV']
    data = pd.DataFrame([sample], columns=columns)
    probability = Rain_model.predict_proba(data)
    chance=int(probability[0][1]*100)
    print(chance)
