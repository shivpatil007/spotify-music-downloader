
import urllib.request
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import imp_functions
import unidecode

cid = os.environ.get('cid')
csecret = os.environ.get('csecret')
client_credentials_manager = SpotifyClientCredentials(
    client_id=cid, client_secret=csecret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_number(playlist_link):
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    song_number = len(sp.playlist_tracks(playlist_URI)["items"])
    print(song_number)
    return song_number


def single_track_download(track_link):
    trac_URI = track_link.split("/")[-1].split("?")[0]
    track = sp.track(trac_URI)
    music_name = track["name"]+" " + \
        sp.artist(track["artists"][0]["uri"])['name']
    music_name = unidecode.unidecode(music_name)
    music_name = imp_functions.replacesomthing(music_name)
    return "+".join(music_name.split(" "))


def spplaylist_track_record(playlist_link):

    tracks = []
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        music_name = "+".join((track["track"]["name"] + " " +
                               sp.artist(track["track"]["artists"][0]["uri"])['name']).split(" "))
        music_name = unidecode.unidecode(music_name)
        music_name = imp_functions.replacesomthing(music_name)
        tracks.append(music_name)
    return tracks


def youtube_part(music_name):
    from pytube.__init__ import YouTube
    import re
    print(music_name)
    try:
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query="+music_name)
        video_uls = "https://www.youtube.com/watch?v=" + \
            re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
        yt = YouTube(video_uls)
        video = yt.streams.filter(only_audio=True).first()

    except Exception as e:
        print(e)
        print("No video found")
        return False
    return video


def spoti_tube(music_name, id):
    try:
        video = youtube_part(music_name)
        out_file = video.download(output_path=os.getcwd()+"/music"+id)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    except:
        print("except done")
    music_name = music_name.replace("+", " ")
    return 'currently <h4>"'+music_name+'"</h4> is being converted...'


def creating_zip(id):
    from zipfile import ZipFile
    from threading import Thread
    id = str(id)
    plalist_songs_name = os.listdir("music"+id)
    try:
        with ZipFile('playlist'+id+'.zip', 'w') as myzip:
            for song in plalist_songs_name:
                myzip.write(os.getcwd()+"/music"+id + '/'+song)
        myzip.close()
    except Exception as e:
        print(e)

    #Thread(target=imp_functions.deleting, args=(id,)).start()
    print("Done")


link = 'https://open.spotify.com/track/7rglLriMNBPAyuJOMGwi39?si=85a0cb5821074532'
single_track_download(link)
