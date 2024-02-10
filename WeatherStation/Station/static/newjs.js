var prevbox=document.getElementById('Humidity');
var tempid = localStorage.getItem('tempid') || 404;
var trar = localStorage.getItem('trar') || 1;
var ar=tempid
thevalues={}
function nextpagedata(data) {
    tempid = data;
    ar=tempid
    localStorage.setItem('tempid', tempid);
    window.location.href = "/details";
}
function updatemain(newdata){
    thevalues=newdata;
    prevbox=document.getElementById('Humidity');
}

function checkvalue(n,id,dorw,lastdate2){
    ar=tempid;
    var lefty=document.getElementById('leftgo');
    var rigthty=document.getElementById('rigthgo');
    if(id==404)
    {
        if(n==0){
            if(trar==1){
                lefty.classList.add('invalidmove')
            }
            else{
                trar--;
                lefty.classList.add('validmoveL')
            }
        }
        else{
            if(trar==11){
                rigthty.classList.add('invalidmove')
            }
            else{
                trar++;
                rigthty.classList.add('validmoveR')
            }
        }
        topvaluesupdate(dorw,thevalues['Name'][trar],thevalues['Value'][trar],thevalues['symbol'][trar],thevalues['Date'][trar],lastdate2)
    }
    else{
    if(n==0){
        if(ar==1){
            lefty.classList.add('invalidmove')
        }
        else{
            lefty.classList.add('validmoveL')
            ar--;
        }
    }
    else{
        if(ar==11){
            rigthty.classList.add('invalidmove')
        }
        else{
            rigthty.classList.add('validmoveR')
            ar++;
        }
    }
    perdevicedeatils(ar,1)}
    setTimeout(() => {
        if (lefty.classList.contains('validmoveL')) {
            lefty.classList.remove('validmoveL');}
      }, 500);
      setTimeout(() => {
        if (rigthty.classList.contains('validmoveR')) {
            rigthty.classList.remove('validmoveR');}
      }, 500);
      setTimeout(() => {
        if (lefty.classList.contains('invalidmove')) {
            lefty.classList.remove('invalidmove');}
      }, 500);
      setTimeout(() => {
        if (rigthty.classList.contains('invalidmove')) {
            rigthty.classList.remove('invalidmove');}
      }, 500);
}

function topvaluesupdate(dorw,devicenameout,maxvalue,maxvalue_symbol,maxvalue_date,lastdate2)
{
    if(prevbox){
    prevbox.style.transform="scale(1)";}
    Databox=document.getElementById(devicenameout);
    if(Databox){
        Databox.style.transform="scale(1.2)";
        prevbox=Databox
    }
    $("#de_name").text(devicenameout);
          $("#de_value").text(maxvalue + maxvalue_symbol);
          if(dorw==0){
            if(maxvalue_date)
            {
            predate=lastdate2+" "+maxvalue_date+":00"}
            else{
              predate="No Data"
            }
          }
          else{
            if(maxvalue_date)
            {
              predate=maxvalue_date
            }
            else{
              predate="No Data"
            }
          }
          $("#de_date").text(predate);
}


