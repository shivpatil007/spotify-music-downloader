
import glob
import json
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


def music_name_extractor(track):
    music_name = track["name"]+" " + \
        sp.artist(track["artists"][0]["uri"])['name']
    music_name = unidecode.unidecode(music_name)
    music_name = imp_functions.replacesomthing(music_name)
    return "+".join(music_name.split(" "))


def link_extractor(link):
    link = link.split("/")[-1].split("?")[0]
    return link


def single_track_download(track_link):
    return music_name_extractor(sp.track(link_extractor(track_link)))


def artist_top_tracks(link):
    return [music_name_extractor(track) for track in sp.artist_top_tracks(link_extractor(link))["tracks"]]


def spplaylist_track_record(playlist_link):
    return [music_name_extractor(i["track"]) for i in sp.playlist_tracks(link_extractor(playlist_link))["items"]]


def get_album_tracks(album_link):
    return [music_name_extractor(track) for track in sp.album_tracks(link_extractor(album_link))["items"]]


def youtube_part(vedio_id, id):
    from pytube.__init__ import YouTube
    try:

        video_uls = "https://www.youtube.com/watch?v=" + vedio_id
        yt = YouTube(video_uls)
        video = yt.streams.filter(only_audio=True).first().download(
            output_path=os.getcwd()+"/music"+id)
        base, ext = os.path.splitext(video)
        new_file = base + '.mp3'
        os.rename(video, new_file)
        return 'currently <h4>"'+yt.title+'"</h4> is being converted...'
    except Exception as e:
        print(e)


def spoti_tube(music_name, id):
    import re
    try:
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query="+music_name)
        vedio_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())[0]
        youtube_part(vedio_id, id)
    except Exception as e:
        print(e)
    music_name = music_name.replace("+", " ")
    return 'currently <h4>"'+music_name+'"</h4> is being converted...'


def creating_zip(id, plalist_songs_name):
    from zipfile import ZipFile
    id = str(id)
    try:
        with ZipFile('playlist'+id+'.zip', 'w') as myzip:
            for song in plalist_songs_name:
                myzip.write(os.getcwd()+"/music"+id + '/'+song)
        myzip.close()
    except Exception as e:
        print(e)
    print("Done")


def main_spotify_downloder(data):
    info = imp_functions.analyse_link_of_spotify_or_youtube(data)
    if info == 'sp-playlist':
        tracks = spplaylist_track_record(data)
    elif info == 'sp-track':
        tracks = [single_track_download(data)]
    elif info == 'sp-artist':
        tracks = artist_top_tracks(data)
    elif info == 'sp-album':
        tracks = get_album_tracks(data)
    return tracks


def yt_playlist(data):
    from pytube.__init__ import Playlist
    try:
        return [i.split("=")[-1] for i in Playlist(data)]
    except Exception as e:
        print(e)
