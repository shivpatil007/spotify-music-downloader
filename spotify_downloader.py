import re
import urllib.request
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube.__init__ import YouTube
from zipfile import ZipFile
import unidecode


cid = os.getenv('CID')
csecret = os.getenv('CSECRET')
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
linkk = "https://open.spotify.com/playlist/37i9dQZF1EpR4uXT7fbqOP?si=bbbf8ce564cd4aff"


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


tracks = []
plalist_songs_name = []


def track_record(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        tracks.append(track)
    return 'Getting tracks from playlist'


def spoti_tube():

    track = tracks[0]

    music_name = "+".join((track["track"]["name"] + " " +
                           sp.artist(track["track"]["artists"][0]["uri"])['name']).split(" "))

    music_name = unidecode.unidecode(music_name)
    music_name = replacesomthing(music_name)
    print(music_name + str(len(tracks)))
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

    except:
        print("Error")
    if tracks:
        tracks.pop(0)
    print("except done")
    return 'currently <h4>"'+track["track"]["name"]+'"</h4> is being converted...'


def creating_zip():
    plalist_songs_name = os.listdir("music")
    with ZipFile('plalylist.zip', 'w') as myzip:
        for song in plalist_songs_name:
            myzip.write('music/'+song)
    myzip.close()
    plalist_songs_name = []
    print("Done")
