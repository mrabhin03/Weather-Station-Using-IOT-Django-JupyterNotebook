def device_limitsdata():
    device_limits = {
            'limits': [{ #0 default
                'High': 20,
                'Mid': 10,
                'Low': 5
            },
            {
                #1 Humidity Sensor
                'HighColor':"red",
                'High': 90,
                'MtoHColor':"orange",
                'Mid': 85,
                'LtoMColor':"rgb(81, 159, 226)",
                'Low': 50,
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
                #4 Sun Light
                'HighColor':"rgb(255, 53, 53)",
                'High': 90, 
                'MtoHColor':"yellow",
                'Mid': 60,
                'LtoMColor':"yellow",
                'Low': 25,
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
                #7 Moisture
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
                'Mid': 700,
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
    return device_limits
def weekdays():
    day_names = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }
    return day_names
def device_names_get():
    device_names = ["","Humidity","Temperature","Sound","Sun Light","Chance of Rain","Wind Speed","Moisture","Atmospheric Pressure","UV","Wind Direction","PM 2.5"]
    return device_names

def icon_get():
    symbols_data = ["","%","°C","%","%","%","km/h","%","hPa","%","°"," µg/m³"]
    return symbols_data

def device_icon_name_get():
    device_icon = ["","cloudy-outline","thermometer-outline","volume-high-outline","sunny-outline","umbrella-outline","speedometer-outline","logo-electron","contract-outline","warning-outline","compass-outline","balloon"]
    return device_icon

def rain_icon_convertion(rain_data):
    data2_value = int(rain_data)
    if data2_value >=75:
        rain="rainy-outline"
    elif data2_value >=50:
        rain="cloudy-outline"
    elif data2_value >=30:
        rain="partly-sunny-outline"
    else:
        rain="sunny-outline"
    return rain