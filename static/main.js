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

async function aTestFunction() {
    id
    await fetch(
        window.location.origin + '/get_playlist_songs_no', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'id': id })
    })
        .then(res => res.json())
        .then(async out1 => {
            while (out1.songs_number--) {
                await fetch(window.location.origin + '/songgs_download', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 'id': id, 'song_no': out1.songs_number + 1 })
                })
                    .then(res => res.json())
                    .then(out => {
                        if (out.message != "") {
                            document.getElementById("track-name").innerHTML = out.message;
                        }
                        else {
                            document.getElementById("load").style.display = 'none';
                            document.getElementById("final-dow").style.display = 'block';
                        }

                    }
                    )
                    .catch(err => 'Something went wrong');
            }

        })
        .catch(err => 'Something went wrong');
    // The image is ready!
}

