function actualiser() {
    //window.location.reload(true);
    alert("teste");

}

function timedRefresh(timeoutPeriod) {
	setTimeout("location.reload(true);",timeoutPeriod);
   
}
window.onload = timedRefresh(5000);
