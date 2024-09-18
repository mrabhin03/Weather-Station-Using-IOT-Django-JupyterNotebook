import random
device_values = {
        'values': [{
            'Max': 20,#default
            'Min': 10
        },
        {
            #Humidity
            'Max': 86,
            'Min': 78
        },{
            #Temperature
            'Max': 36,
            'Min': 28
        },{
            #Sound
            'Max': 30,
            'Min': 6
        },{
            #Sun Light
            'Max': 60,
            'Min': 40
        },{
            #Chance of Rain
            'Max': 80,
            'Min': 20
        },{
            #Wind Speed sensor
            'Max': 13,
            'Min': 3
        },{
            #Moisture
            'Max': 86,
            'Min': 78
        },{
            #Atmospheric Pressure
            'Max': 1015,
            'Min': 995
        },{
            #UV Sensor
            'Max': 10,
            'Min': 2
        },{
            #Wind Direction
            'Max': 360,
            'Min': 0
        },{
            #Altitude
            'Max': 126,
            'Min': 124
        },
    ]}
time=[0,3,6,9,12,15,18,21,23]


datefrom=20
dateto=27
month=5

day=datefrom
while day<=dateto:
    temtime=0
    for j in time:
        i=1
        ThetimeH = random.randint(temtime, j)
        if ThetimeH==j and ThetimeH!=0:
            ThetimeH=ThetimeH-1
        ThetimeM = random.randint(10, 58)
        ThetimeS = random.randint(10, 58)
        while i<=11:
            maxvalue=device_values['values'][i]['Max']
            minvalue=device_values['values'][i]['Min']
            Thevalue = random.randint(minvalue, maxvalue)
            thedata=f" INSERT INTO `data_store`( `device_values`, `date_time`, `device_id`) VALUES ('{Thevalue}','2024-{month}-{day} {ThetimeH}:{ThetimeM}:{ThetimeS}','{i}');"
            print(thedata)
            i=i+1
        temtime=j
    day=day+1
