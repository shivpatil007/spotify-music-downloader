function splist(i) {
    if (i==1) {
    document.getElementById("sp-list").innerText="Spotify Playlist Url";
    }
    if (i==2) {
    document.getElementById("sp-list").innerText="Spotify Song Url";
    }
    if (i==3) {
    document.getElementById("sp-list").innerText="Spotify Artist Url";
    }
    if(i==4) {
    document.getElementById("sp-list").innerText="Spotify Album Url";
    }
}

function open_load() {
    document.getElementById("main-page").style.display='none';
    document.getElementById("load").style.display='block';
}



function bgrchange(temp){
    if(temp==1) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/204161-spotify-wallpaper.png)";
}
if(temp==2) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/wallpaper2you_31485.jpg)";
}
}


