var prevbox = document.getElementById("Humidity");
var tempid = localStorage.getItem("tempid") || 404;
var trar = localStorage.getItem("trar") || 1;
var ar = 1;
selcteddv = [1,2,3,4, 5,6,7, 8,9,10,11];
timeout_t1=0
var device_limits = {
  limits: [
    {
      //0 default
      High: 20,
      Mid: 10,
      Low: 5,
      Hightx: "The value above 20 is considered high",
      Modertx: "The value between 10 and 20 is considered moderate",
      GoodTx: "The value between 5 and 10 is considered good",
    },
    {
      //1 Humidity Sensor
      High: "60 - 100%",
      Moder: "30 - 60%",
      Good: "15 - 30%",
      Low: "0 - 15%",
      Lowtx: "The Humidity below 15 are considered as low Humidity",
      Hightx: "The value between 60 and 100 is considered high",
      Modertx: "The value between 30 and 60 is considered moderate",
      GoodTx: "The value between 15 and 30 is considered good",
    },
    {
      //2 Temperature Sensor
      High: "60 - 100°C",
      Moder: "30 - 60°C",
      Good: "15 - 30°C",
      Low: "0 - 15°C",
      Lowtx: "The temperature below 15°C is considered low",
      Hightx: "The temperature between 60°C and 100°C is considered high",
      Modertx: "The temperature between 30°C and 60°C is considered moderate",
      GoodTx: "The temperature between 15°C and 30°C is considered good",
    },
    {
      //3 PM2.5 Sensor
      High: "60 - 100%",
      Moder: "30 - 60%",
      Good: "15 - 30%",
      Low: "0 - 15%",
      Lowtx: "The PM2.5 level below 15 is considered low",
      Hightx: "The PM2.5 level above 60 is considered high",
      Modertx: "The PM2.5 level between 30 and 60 is considered moderate",
      GoodTx: "The PM2.5 level between 15 and 30 is considered good",
    },
    {
      //4 Sun Light
      High: "> 20%",
      Moder: "5 - 20%",
      Good: "2 - 5%",
      Low: "< 2%",
      Lowtx: "The Sun Light level below 2 is considered low",
      Hightx: "The Sun Light level above 20 is considered high",
      Modertx: "The Sun Light level between 5 and 20 is considered moderate",
      GoodTx: "The Sun Light level between 2 and 5 is considered good",
    },
    {
      //5 Chance of Rain
      High: "75 - 100%",
      Moder: "50 - 75%",
      Good: "25 - 50%",
      Low: "0 - 25%",
      Lowtx: "The chance of rain is Very Low",
      Hightx: "The chance of rain is Very High",
      Modertx: "The chance of rain is High",
      GoodTx: "The chance of rain is Low",
    },
    {
      //6 Wind Speed sensor
      High: "> 25km/h",
      Moder: "12 - 25km/h",
      Good: "5 - 12km/h",
      Low: "< 5km/h",
      Lowtx: "The wind speed below 5 km/h is considered low",
      Hightx: "The wind speed above 25 km/h is considered high",
      Modertx:
        "The wind speed between 12 km/h and 25 km/h is considered moderate",
      GoodTx: "The wind speed between 5 km/h and 12 km/h is considered good",
    },
    {
      //7 Moisture Sensor
      High: "> 20%",
      Moder: "10 - 20%",
      Good: "5 - 10%",
      Low: "< 5%",
      Lowtx: "The Moisture level below 5 is considered low",
      Hightx: "The Moisture level above 20 is considered high",
      Modertx: "The Moisture level between 10 and 20 is considered moderate",
      GoodTx: "The Moisture level between 5 and 10 is considered good",
    },
    {
      //8 Atmospheric Pressure
      High: "> 1013hPa",
      Moder: "980 - 1013hPa",
      Good: "550 - 980hPa",
      Low: "< 550hPa",
      Lowtx: "The atmospheric pressure below 550 is considered low",
      Hightx: "The atmospheric pressure above 1013 is considered high",
      Modertx:
        "The atmospheric pressure between 980 and 1013 is considered moderate",
      GoodTx: "The atmospheric pressure between 550 and 980 is considered good",
    },
    {
      //9 UV Sensor
      High: "> 40%",
      Moder: "20 - 40%",
      Good: "10 - 20%",
      Low: "< 10%",
      Lowtx: "The UV index below 10 is considered low",
      Hightx: "The UV index above 40 is considered high",
      Modertx: "The UV index between 20 and 40 is considered moderate",
      GoodTx: "The UV index between 10 and 20 is considered good",
    },
    {
      //10 Wind Direction
      High: "> 60",
      Moder: "30 - 60",
      Good: "15 - 30",
      Low: "< 15",
      Lowtx: "The wind direction below 15° is considered low",
      Hightx: "The wind direction above 60° is considered high",
      Modertx: "The wind direction between 30° and 60° is considered moderate",
      GoodTx: "The wind direction between 15° and 30° is considered good",
    },
    {
      //11 Altitude
      High: "> 30m",
      Moder: "20 - 30m",
      Good: "15 - 20m",
      Low: "< 15m",
      Lowtx: "The Altitude below 15 meter is considered low",
      Hightx: "The Altitude above 30 meter is considered high",
      Modertx: "The Altitude between 20 and 30 meter is considered moderate",
      GoodTx: "The Altitude between 15 and 20 meter is considered good",
    },
  ],
};


maxdatabase = {};
mindatabase = {};
averagebase={};


function nextpagedata(data, trar) {
  tempid = data;
  localStorage.setItem("tempid", tempid);
  localStorage.setItem("trar", trar);
  window.location.href = "/details";
}
function updatemain(maxdata, mindata,average,color_data) {
  maxdatabase = maxdata;
  mindatabase = mindata;
  averagebase=average;
  colorbase=color_data;
  prevbox = document.getElementById("Humidity");
}

var themovesobject = [];
alldevs = [0, 1, 2, 4, 6, 7, 9, 11];
buttonaray=[0, 1, 2, 4, 6, 7, 9, 11]

function checkvalue(n, id, dorw, lastdate2, themainelemantdata,newval) {
  timeout_t1=300
  trar=parseInt(trar)
  if(trar>alldevs.length){trar=alldevs.indexOf(trar);}
  
  themovesobject[0] = document.getElementById("max_data_name");
  themovesobject[1] = document.getElementById("max_data_value");
  themovesobject[2] = document.getElementById("max_data_value_sy");
  themovesobject[3] = document.getElementById("max_data_date");

  themovesobject[4] = document.getElementById("pre_name");
  themovesobject[5] = document.getElementById("pre_value");
  themovesobject[6] = document.getElementById("pre_value_sy");
  themovesobject[7] = document.getElementById("pre_date");

  themovesobject[8] = document.getElementById("min_data_name");
  themovesobject[9] = document.getElementById("min_data_value");
  themovesobject[10] = document.getElementById("min_data_value_sy");
  themovesobject[11] = document.getElementById("min_data_date");
  if(themainelemantdata==0){
    trar=parseInt(newval)
    trar=alldevs.indexOf(trar)
    topvaluesupdate(
      dorw,
      maxdatabase["Name"][alldevs[trar]],
      maxdatabase["Value"][alldevs[trar]],
      maxdatabase["symbol"][alldevs[trar]],
      maxdatabase["Date"][alldevs[trar]],
      lastdate2,
      1,
      1
    );
    topvaluesupdate(
      dorw,
      mindatabase["Name"][alldevs[trar]],
      mindatabase["Value"][alldevs[trar]],
      mindatabase["symbol"][alldevs[trar]],
      mindatabase["Date"][alldevs[trar]],
      lastdate2,
      0,
      1
    );
  }
  else{
    theelemantdata = themainelemantdata.querySelector("#arrowint");
  if (id == 404) {
    if (n == 0) {
      if (trar == 1) {
        theelemantdata.classList.add("invalidmove");
      } else {
        trar--;
        theelemantdata.classList.add("validmoveL");
        for (i in themovesobject) {
          themovesobject[i].classList.add("textleftout");
        }
        setTimeout(() => {
          for (i in themovesobject) {
            themovesobject[i].classList.remove("textleftout");
          }
          for (i in themovesobject) {
            themovesobject[i].classList.add("textleftin");
          }
        }, 200);
      }
    } else {
      if (trar >= alldevs.length-1) {
        theelemantdata.classList.add("invalidmove");
      } else {
        trar++;
        theelemantdata.classList.add("validmoveR");
        for (i in themovesobject) {
          themovesobject[i].classList.add("textrigthout");
        }
        setTimeout(() => {
          for (i in themovesobject) {
            themovesobject[i].classList.remove("textrigthout");
          }
          for (i in themovesobject) {
            themovesobject[i].classList.add("textrigthin");
          }
        }, 200);
      }
    }
    topvaluesupdate(
      dorw,
      maxdatabase["Name"][alldevs[trar]],
      maxdatabase["Value"][alldevs[trar]],
      maxdatabase["symbol"][alldevs[trar]],
      maxdatabase["Date"][alldevs[trar]],
      lastdate2,
      1,
      1
    );
    topvaluesupdate(
      dorw,
      mindatabase["Name"][alldevs[trar]],
      mindatabase["Value"][alldevs[trar]],
      mindatabase["symbol"][alldevs[trar]],
      mindatabase["Date"][alldevs[trar]],
      lastdate2,
      0,
      1
    );
  } else {
    a = 0;
    if (n == 0) {
      if (ar == 0) {
        theelemantdata.classList.add("invalidmove");
      } else {
        for (i in themovesobject) {
          themovesobject[i].classList.add("textleftout");
        }
        setTimeout(() => {
          for (i in themovesobject) {
            themovesobject[i].classList.remove("textleftout");
          }
          for (i in themovesobject) {
            themovesobject[i].classList.add("textleftin");
          }
        }, 200);
        theelemantdata.classList.add("validmoveL");
        ar--;
      }
    } else {
      if (ar == 10) {
        theelemantdata.classList.add("invalidmove");
      } else {
        theelemantdata.classList.add("validmoveR");
        ar++;
        for (i in themovesobject) {
          themovesobject[i].classList.add("textrigthout");
        }
        setTimeout(() => {
          for (i in themovesobject) {
            themovesobject[i].classList.remove("textrigthout");
          }
          for (i in themovesobject) {
            themovesobject[i].classList.add("textrigthin");
          }
        }, 200);
      }
    }

    perdevicedeatils(selcteddv[ar], 1);
  }

  setTimeout(() => {
    if (theelemantdata.classList.contains("validmoveL")) {
      theelemantdata.classList.remove("validmoveL");
    }
    if (theelemantdata.classList.contains("validmoveR")) {
      theelemantdata.classList.remove("validmoveR");
    }
    if (theelemantdata.classList.contains("invalidmove")) {
      theelemantdata.classList.remove("invalidmove");
    }
    if (themovesobject[0].classList.contains("textleftin")) {
      for (i in themovesobject) {
        themovesobject[i].classList.remove("textleftin");
      }
    }
    if (themovesobject[0].classList.contains("textrigthin")) {
      for (i in themovesobject) {
        themovesobject[i].classList.remove("textrigthin");
      }
    }
  }, 500);
}
}

function topvaluesupdate(
  dorw,
  devicenameout,
  value,
  symbol,
  value_date,
  lastdate2,
  nav,
  thar,
  id,
  avg
) {
  setTimeout(() => {
    if (thar == 1) {
      
      trar=parseInt(trar)
      if(trar>alldevs.length){trar=alldevs.indexOf(trar);}
      idv=alldevs[trar]
      average_data=averagebase["value"][idv]
      
      
    } else {
      idv = id;
      average_data=avg
    }
    if (prevbox) {
      prevbox.classList.remove("sel")
    }
    Databox = document.getElementById(devicenameout);
    if (Databox) {
      Databox.classList.add("sel")
      prevbox = Databox;
    }
    if (nav == 1) {
      dename = "max_data_name";
      devalue = "max_data_value";
      desyml="max_data_value_sy";
      dedate = "max_data_date";
    } else {
      dename = "min_data_name";
      devalue = "min_data_value";
      desyml="min_data_value_sy";
      dedate = "min_data_date";
    }
    $("#pre_name").text(devicenameout);
    $("#" + dename).text(devicenameout);
    $("#" + devalue).text(value);
    $("#" + desyml).text(symbol);
    $("#pre_value").text(average_data);
    $("#pre_value_sy").text(symbol);
    if (dorw == 0) {
      if (value_date) {
        predate = lastdate2 + " " + value_date + ":00";
        Predates=lastdate2
      } else {
        Predates=predate = "No Data";
      }
    } else {
      if (value_date) {
        predate = value_date;
        Predates="This Week"
      } else {
        Predates=predate = "No Data";
      }
    }
    $("#" + dedate).text(predate);
    $("#pre_date").text(Predates);

    if (id == 5) {
      $("#til").text("Very Low Chance");
      $("#tig").text("Low Chance");
      $("#tim").text("High Chance");
      $("#tih").text("Very High Chance");
    } else {
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
    
  }, timeout_t1);
}
var perdevice = [0, 1, 2, 5];
var iva=2
function homegraphdata(nav, obj) {
  arrowdata = obj.querySelector("#homeswitch");
  if (nav == 0) {
    if (iva == 1) {
      arrowdata.classList.add("invalidmove");
    } else {
      arrowdata.classList.add("validmoveL");
      iva--;
      if (iva == 10) {
        iva--;
      }
    }
  } else {
    if (iva == 3) {
      arrowdata.classList.add("invalidmove");
    } else {
      arrowdata.classList.add("validmoveR");
      iva++;
      if (iva == 10) {
        iva++;
      }
    }
  }
  didval=perdevice[iva]
  graphupdates(didval);
  setTimeout(() => {
    if (arrowdata.classList.contains("validmoveL")) {
      arrowdata.classList.remove("validmoveL");
    }
    if (arrowdata.classList.contains("validmoveR")) {
      arrowdata.classList.remove("validmoveR");
    }
    if (arrowdata.classList.contains("invalidmove")) {
      arrowdata.classList.remove("invalidmove");
    }
  }, 500);
}

function themecheck()
{
    let getMode = localStorage.getItem("mode");
    const body = document.querySelector("body")
    if (getMode && getMode === "dark") {
        switchval=document.getElementById("switchdata");
        switchval.classList.add("dark");
        imagedata=document.getElementById("imagedata")
        imagedata.src="/Main/Backgroundicondark.png";
      }
      else{
        body.classList.remove("dark");
        setTimeout(() => {chartcolorchange();}, 200);
        imagedata.src="/Main/Backgroundicon.png";
      }
}


function themechange()
{
  
    chartdata=needchart();
    switchval=document.getElementById("switchdata");
    body_data=document.querySelector("body");
    imagedata=document.getElementById("imagedata")
    if(body_data.classList.contains("dark"))
    {
        imagedata.src="/Main/Backgroundicon.png";
        body_data.classList.remove("dark")
        switchval.classList.remove("dark");
        if(chartdata!=0){
          chartdata.options.scales.x.grid.color=chartdata.options.scales.y.grid.color = 'rgba(0, 0, 0, 0.07)';
          chartdata.options.scales.x.ticks.color=chartdata.options.scales.y.ticks.color = 'black';
        }
        localStorage.setItem("mode", "light");
    }
    else{
        imagedata.src="/Main/Backgroundicondark.png";
        if(chartdata!=0){
          chartdata.options.scales.x.grid.color=chartdata.options.scales.y.grid.color = 'rgba(255, 255, 255, 0.1)';
          chartdata.options.scales.x.ticks.color=chartdata.options.scales.y.ticks.color = 'white';
        }
        body_data.classList.add("dark")
        switchval.classList.add("dark");
        localStorage.setItem("mode", "dark");
    }
    chartdata.update();
}

