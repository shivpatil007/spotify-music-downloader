import imp
import re
import urllib.request
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
import config
cid = config.cid
secret = config.secret


def spoti_tube():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlist_link = "https://open.spotify.com/playlist/62GAcyFWeutrREPqFeYIxV?si=2c9263dfa2e948b8"
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]

    for track in sp.playlist_tracks(playlist_URI)["items"]:

        music_name = "+".join((track["track"]["name"] + " " +
                               sp.artist(track["track"]["artists"][0]["uri"])['name']).split(" "))
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query="+music_name)
        video_uls = "https://www.youtube.com/watch?v=" + \
            re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
        yt = YouTube(video_uls)
        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download(output_path=os.getcwd())

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    print("Done")
