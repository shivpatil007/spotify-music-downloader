function splist(t1,t2,t3,t4) {
  
    document.getElementById("sp-list").style.display=t1;
    document.getElementById("sp-song").style.display=t2;
    document.getElementById("yt-list").style.display=t3;
    document.getElementById("yt-song").style.display=t4;


}

function open_load() {
    document.getElementById("main-page").style.display='none';
    document.getElementById("load").style.display='block';
}


async function  call_songs() {
    
    await fetch(window.location.origin+'/get_playlist_songs_no')
    .then(res => res.json())
    .then(async out1 =>
        {   
            while(out1.songs_number--)
            {
              await  fetch(window.location.origin+'/songgs_download')
                .then(res => res.json())
                .then(out =>
                    {  
                         if (out.message!=""){
                            document.getElementById("track-name").innerHTML = out.message;
                        }
                        else{
                            document.getElementById("load").style.display='none';
                            document.getElementById("final-dow").style.display='block';
                        }
                        
                    }
                    )
                .catch(err => 'Something went wrong');
            }

        } )
    .catch(err => 'Something went wrong');
}

function bgrchange(temp){
    if(temp==1) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/204161-spotify-wallpaper.png)";
}
if(temp==2) {
    document.getElementById("bgr").style.backgroundImage = "url(static/images/wallpaper2you_31485.jpg)";
}
}


