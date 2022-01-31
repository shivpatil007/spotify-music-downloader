function splist(temp) {
    if(temp==1) {
    document.getElementById("sp-list").style.display="block";
    document.getElementById("sp-song").style.display="none";
    document.getElementById("yt-list").style.display="none";
    document.getElementById("yt-song").style.display="none";
}
if(temp=="2") {
    document.getElementById("sp-list").style.display="none";
    document.getElementById("sp-song").style.display="block";
    document.getElementById("yt-list").style.display="none";
    document.getElementById("yt-song").style.display="none";
}
if(temp=="3") {
    document.getElementById("sp-list").style.display="none";
    document.getElementById("sp-song").style.display="none";
    document.getElementById("yt-list").style.display="block";
    document.getElementById("yt-song").style.display="none";
}
if(temp=="4") {
    document.getElementById("sp-list").style.display="none";
    document.getElementById("sp-song").style.display="none";
    document.getElementById("yt-list").style.display="none";
    document.getElementById("yt-song").style.display="block";
}

}