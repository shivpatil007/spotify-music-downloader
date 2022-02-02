import re
import urllib.request
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube.__init__ import YouTube
from zipfile import ZipFile
from boto.s3.connection import S3Connection
import unidecode

cid = os.environ.get('cid')
csecret = os.environ.get('csecret')
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
linkk = "https://open.spotify.com/playlist/62GAcyFWeutrREPqFeYIxV?si=2c9263dfa2e948b8"


def get_song_number(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    song_number = len(sp.playlist_tracks(playlist_URI)["items"])
    print(song_number)
    return song_number


def replacesomthing(text):
    a = {
        'å': 'a',
        'ä': 'a',
        'ö': 'o',
        'Ö': 'O',
        'À': 'A',
        'Á': 'A',
        'Â': 'A',
        'Ã': 'A',
        'Ä': 'A',
        'Å': 'A',
        'Æ': 'A',
    }

    for i in a:
        text = text.replace(i, a[i])
    return text


def spoti_tube(playlist_link):
    print(playlist_link)
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    plalist_songs_name = []

    for track in sp.playlist_tracks(playlist_URI)["items"]:

        music_name = "+".join((track["track"]["name"] + " " +
                               sp.artist(track["track"]["artists"][0]["uri"])['name']).split(" "))

        music_name = unidecode.unidecode(music_name)
        music_name = replacesomthing(music_name)

        try:
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
        except:
            print("Error")
    with ZipFile('plalylist.zip', 'w') as myzip:
        for song in plalist_songs_name:
            myzip.write(song)
    myzip.close()

    print("Done")
