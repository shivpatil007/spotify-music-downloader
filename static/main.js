function splist(t1,t2,t3,t4) {
  
    document.getElementById("sp-list").style.display=t1;
    document.getElementById("sp-song").style.display=t2;
    document.getElementById("yt-list").style.display=t3;
    document.getElementById("yt-song").style.display=t4;


}


function bgrchange(temp){
    if(temp==1) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/204161-spotify-wallpaper.png)";
}
if(temp==2) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/wallpaper2you_31485.jpg)";
}
}


