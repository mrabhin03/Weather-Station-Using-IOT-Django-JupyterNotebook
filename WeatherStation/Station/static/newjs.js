var prevbox=document.getElementById('Humidity');
var tempid = localStorage.getItem('tempid') || 404;
var trar = localStorage.getItem('trar') || 1;
var ar=1
selcteddv=[3,5,8];

var device_limits = {
    'limits': [
        { //0 default
            'High': 20,
            'Mid': 10,
            'Low': 5,
            'Hightx': "The value above 20 is considered high",
            'Modertx': "The value between 10 and 20 is considered moderate",
            'GoodTx': "The value between 5 and 10 is considered good"
        },
        { //1 Humidity Sensor
            'High': "60 - 100%",
            'Moder': "30 - 60%",
            'Good': "15 - 30%",
            'Low': "0 - 15%",
            'Lowtx': "The Humidity below 15 are considered as low Humidity",
            'Hightx': "The value between 60 and 100 is considered high",
            'Modertx': "The value between 30 and 60 is considered moderate",
            'GoodTx': "The value between 15 and 30 is considered good"
        },
        { //2 Temperature Sensor
            'High': "60 - 100°C",
            'Moder': "30 - 60°C",
            'Good': "15 - 30°C",
            'Low': "0 - 15°C",
            'Lowtx': "The temperature below 15°C is considered low",
            'Hightx': "The temperature between 60°C and 100°C is considered high",
            'Modertx': "The temperature between 30°C and 60°C is considered moderate",
            'GoodTx': "The temperature between 15°C and 30°C is considered good"
        },
        { //3 Sound Sensor
            'High': "60 - 100%",
            'Moder': "30 - 60%",
            'Good': "15 - 30%",
            'Low': "0 - 15%",
            'Lowtx': "The sound level below 15 is considered low",
            'Hightx': "The sound level above 60 is considered high",
            'Modertx': "The sound level between 30 and 60 is considered moderate",
            'GoodTx': "The sound level between 15 and 30 is considered good"
        },
        { //4 Co2 Sensor
            'High': "> 20%",
            'Moder': "5 - 20%",
            'Good': "2 - 5%",
            'Low': "< 2%",
            'Lowtx': "The CO2 level below 2 is considered low",
            'Hightx': "The CO2 level above 20 is considered high",
            'Modertx': "The CO2 level between 5 and 20 is considered moderate",
            'GoodTx': "The CO2 level between 2 and 5 is considered good"
        },
        { //5 Chance of Rain
            'High': "75 - 100%",
            'Moder': "50 - 75%",
            'Good': "25 - 50%",
            'Low': "0 - 25%",
            'Lowtx': "The chance of rain is Very Low",
            'Hightx': "The chance of rain is Very High",
            'Modertx': "The chance of rain is High",
            'GoodTx': "The chance of rain is Low"
        },
        { //6 Wind Speed sensor
            'High': "> 25km/h",
            'Moder': "12 - 25km/h",
            'Good': "5 - 12km/h",
            'Low': "< 5km/h",
            'Lowtx': "The wind speed below 5 km/h is considered low",
            'Hightx': "The wind speed above 25 km/h is considered high",
            'Modertx': "The wind speed between 12 km/h and 25 km/h is considered moderate",
            'GoodTx': "The wind speed between 5 km/h and 12 km/h is considered good"
        },
        { //7 NO2 Sensor
            'High': "> 20%",
            'Moder': "10 - 20%",
            'Good': "5 - 10%",
            'Low': "< 5%",
            'Lowtx': "The NO2 level below 5 is considered low",
            'Hightx': "The NO2 level above 20 is considered high",
            'Modertx': "The NO2 level between 10 and 20 is considered moderate",
            'GoodTx': "The NO2 level between 5 and 10 is considered good"
        },
        { //8 Atmospheric Pressure
            'High': "> 1013hPa",
            'Moder': "980 - 1013hPa",
            'Good': "550 - 980hPa",
            'Low': "< 550hPa",
            'Lowtx': "The atmospheric pressure below 550 is considered low",
            'Hightx': "The atmospheric pressure above 1013 is considered high",
            'Modertx': "The atmospheric pressure between 980 and 1013 is considered moderate",
            'GoodTx': "The atmospheric pressure between 550 and 980 is considered good"
        },
        { //9 UV Sensor
            'High': "> 40%",
            'Moder': "20 - 40%",
            'Good': "10 - 20%",
            'Low': "< 10%",
            'Lowtx': "The UV index below 10 is considered low",
            'Hightx': "The UV index above 40 is considered high",
            'Modertx': "The UV index between 20 and 40 is considered moderate",
            'GoodTx': "The UV index between 10 and 20 is considered good"
        },
        { //10 Wind Direction
            'High': "> 60",
            'Moder': "30 - 60",
            'Good': "15 - 30",
            'Low': "< 15",
            'Lowtx': "The wind direction below 15° is considered low",
            'Hightx': "The wind direction above 60° is considered high",
            'Modertx': "The wind direction between 30° and 60° is considered moderate",
            'GoodTx': "The wind direction between 15° and 30° is considered good"
        },
        { //11 Air Quality
            'High': "AQI > 30",
            'Moder': "AQI 20 - 30",
            'Good': "AQI 15 - 20",
            'Low': "AQI < 15",
            'Lowtx': "The air quality index below 15 is considered low",
            'Hightx': "The air quality index above 30 is considered high",
            'Modertx': "The air quality index between 20 and 30 is considered moderate",
            'GoodTx': "The air quality index between 15 and 20 is considered good"
        },
    ]
};



maxdatabase={}
mindatabase={}

function nextpagedata(data,trar) {
    tempid = data;
    localStorage.setItem('tempid', tempid);
    localStorage.setItem('trar', trar);
    window.location.href = "/details";
}
function updatemain(maxdata,mindata){
    maxdatabase=maxdata;
    mindatabase=mindata;
    prevbox=document.getElementById('Humidity');
}

function checkvalue(n,id,dorw,lastdate2,themainelemantdata){
    theelemantdata=themainelemantdata.querySelector('#arrowint')
    var a
    if(id==404)
    {
        if(n==0){
            if(trar==1){
                theelemantdata.classList.add('invalidmove');
            }
            else{
                if(trar-1==10||trar-1==8||trar-1==3||trar-1==5){
                    trar-=2;
                }
                else{
                trar--;}
                theelemantdata.classList.add('validmoveL')
            }
        }
        else{
            if(trar==11){
                theelemantdata.classList.add('invalidmove')
            }
            else{
                if(trar+1==10||trar+1==8||trar+1==5||trar+1==3){
                    trar+=2;
                }
                else{
                trar++;}
                theelemantdata.classList.add('validmoveR')
            }
        }
        topvaluesupdate(dorw,maxdatabase['Name'][trar],maxdatabase['Value'][trar],maxdatabase['symbol'][trar],maxdatabase['Date'][trar],lastdate2,1,1)
        topvaluesupdate(dorw,mindatabase['Name'][trar],mindatabase['Value'][trar],mindatabase['symbol'][trar],mindatabase['Date'][trar],lastdate2,0,1)
    }
        else{
            a=0
        if(n==0){
            if(ar==0){
                theelemantdata.classList.add('invalidmove');
            }
            else{
                theelemantdata.classList.add('validmoveL')
                ar--;
            }
        }
        else{
            if(ar==2){
                theelemantdata.classList.add('invalidmove')
            }
            else{
                theelemantdata.classList.add('validmoveR')
                ar++;

            }
        }
        
        perdevicedeatils(selcteddv[ar],1)
    }

        setTimeout(() => {
            if (theelemantdata.classList.contains('validmoveL')) {
                    theelemantdata.classList.remove('validmoveL');}
            if (theelemantdata.classList.contains('validmoveR')) {
                    theelemantdata.classList.remove('validmoveR');}
            if (theelemantdata.classList.contains('invalidmove')) {
                    theelemantdata.classList.remove('invalidmove');}
        }, 500);
}

function topvaluesupdate(dorw,devicenameout,value,symbol,value_date,lastdate2,nav,thar,id)
{
    if(thar==1){
        idv=trar
    }
    else{
        idv=id;
    }
    if(prevbox){
        prevbox.style.transform="scale(1)";}
    Databox=document.getElementById(devicenameout);
    if(Databox){
        Databox.style.transform="scale(1.2)";
        prevbox=Databox
    }
    if(nav==1){
        dename="max_data_name";
        devalue="max_data_value";
        dedate="max_data_date"
    }
    else{
        dename="min_data_name";
        devalue="min_data_value";
        dedate="min_data_date"
    }
    $("#pre_name").text(devicenameout);
    $("#"+dename).text(devicenameout);
    $("#"+devalue).text(value + symbol);
    $("#pre_value").text("35" + symbol);
        if(dorw==0){
            if(value_date)
            {
            predate=lastdate2+" "+value_date+":00"}
            else{
            predate="No Data"
            }
        }
        else{
            if(value_date)
            {
                predate=value_date
            }
            else{
                predate="No Data"
            }
        }
        if(id==5)
        {
            $("#til").text("Very Low Chance");
            $("#tig").text("Low Chance");
            $("#tim").text("High Chance");
            $("#tih").text("Very High Chance");
        }
        else{
            $("#til").text("Low");
            $("#tig").text("Good");
            $("#tim").text("Moderate");
            $("#tih").text("Unhealthy");
        }
        
        $("#lowtext").text(device_limits.limits[idv].Lowtx);
        $("#goodtext").text(device_limits.limits[idv].GoodTx);
        $("#modtext").text(device_limits.limits[idv].Modertx);
        $("#hightext").text(device_limits.limits[idv].Hightx);

        $("#lowdata").text(device_limits.limits[idv].Low);
        $("#gooddata").text(device_limits.limits[idv].Good);
        $("#moddata").text(device_limits.limits[idv].Moder);
        $("#unhdata").text(device_limits.limits[idv].High);
        $("#"+dedate).text(predate);
        $("#pre_date").text(predate);
}
var perdevice=[0,1,2,5,11];
function homegraphdata(nav,obj){
    arrowdata=obj.querySelector('#homeswitch')
    if(nav==0){
        if(didval==1){
            arrowdata.classList.add('invalidmove');
        }
        else{
            arrowdata.classList.add('validmoveL')
            didval--;
            if(didval==10){didval--}
        }
    }
    else {
        if(didval==4){
            arrowdata.classList.add('invalidmove');
        }
        else{
            arrowdata.classList.add('validmoveR')
            didval++;
            if(didval==10){didval++}
        }
    }
    graphupdates(perdevice[didval])
    setTimeout(() => {
        if (arrowdata.classList.contains('validmoveL')) {
            arrowdata.classList.remove('validmoveL');}
        if (arrowdata.classList.contains('validmoveR')) {
            arrowdata.classList.remove('validmoveR');}
        if (arrowdata.classList.contains('invalidmove')) {
            arrowdata.classList.remove('invalidmove');}
    }, 500);
}


