import re
import urllib.request
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
import config
from zipfile import ZipFile
import threading
cid = config.cid
secret = config.secret
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
linkk = "https://open.spotify.com/playlist/62GAcyFWeutrREPqFeYIxV?si=2c9263dfa2e948b8"


def spoti_tube_thread(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    t1 = threading.Thread(target=get_song_number, args=[playlist_URI])
    t2 = threading.Thread(target=spoti_tube, args=[playlist_URI])
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def get_song_number(playlist_URI):

    song_number = len(sp.playlist_tracks(playlist_URI)["items"])
    print(song_number)


def spoti_tube(playlist_URI):
    plalist_songs_name = []

    for track in sp.playlist_tracks(playlist_URI)["items"]:

        music_name = "+".join((track["track"]["name"] + " " +
                               sp.artist(track["track"]["artists"][0]["uri"])['name']).split(" "))
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query="+music_name)
        video_uls = "https://www.youtube.com/watch?v=" + \
            re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
        yt = YouTube(video_uls)
        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path=os.getcwd()+"/music")

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        plalist_songs_name.append(new_file)

    with ZipFile('plalylist.zip', 'w') as myzip:
        for song in plalist_songs_name:
            myzip.write(song)
    myzip.close()

    print("Done")


spoti_tube_thread(linkk)
