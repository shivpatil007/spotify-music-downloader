import os
import db_connection
from flask import Flask, Response,  request, render_template, send_file
from flask_restful import Resource, Api
import spotify_downloader
import imp_functions

app = Flask(__name__)
api = Api(app)


class Hello(Resource):

    def get(self):
        return Response(response=render_template('index.html'), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']
        info = imp_functions.analyse_link_of_spotify_or_youtube(data)
        if info == 'sp-playlist':
            tracks = spotify_downloader.spplaylist_track_record(data)
        elif info == 'sp-track':
            tracks = [spotify_downloader.single_track_download(data)]
        elif info == 'sp-artist':
            tracks = spotify_downloader.artist_top_tracks(data)
        id = db_connection.db_insertion(tracks)
        return Response(response=render_template('loading.html', id=id), status=200, mimetype="text/html")


class get_playlist_songs_no(Resource):
    def post(self):
        return {'songs_number': len(db_connection.tracks_from_db(request.json['id']))+1}


class songgs_download(Resource):
    def post(self):
        data = request.json
        id = data['id']
        song_no = data['song_no']
        if song_no == 1:
            return {'message': ''}
        track = db_connection.song_name_retrevial(id, song_no)
        track_name = spotify_downloader.spoti_tube(track, str(id))
        return {'message': track_name}


class download_file(Resource):

    def get(self):
        data = request.args.get('id')
        id = str(data)
        plalist_songs_name = os.listdir("music"+id)
        if len(plalist_songs_name) <= 1:
            return send_file('music'+id+'/'+plalist_songs_name[0], as_attachment=True)
        spotify_downloader.creating_zip(id, plalist_songs_name)
        return send_file('playlist'+id+'.zip', as_attachment=True)


api.add_resource(Hello, '/')
api.add_resource(songgs_download, '/songgs_download')
api.add_resource(get_playlist_songs_no, '/get_playlist_songs_no')
api.add_resource(download_file, '/download_file')


# driver function
if __name__ == '__main__':

    app.run(debug=True,)
