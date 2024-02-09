var tempid = localStorage.getItem('tempid') || 404;
function nextpagedata(data) {
    tempid = data;
    localStorage.setItem('tempid', tempid);
    window.location.href = "/details";
}