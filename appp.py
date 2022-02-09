import os
import db_connection
from flask import Flask, Response,  request, render_template, send_file
from flask_restful import Resource, Api
import spotify_downloader

app = Flask(__name__)
api = Api(app)


class Hello(Resource):

    def get(self):
        return Response(response=render_template('first.html'), status=200, mimetype="text/html")


class spotify(Resource):

    def get(self):
        return Response(response=render_template('index.html', mode=1), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']
        id, typee = db_connection.db_insertion(
            spotify_downloader.main_spotify_downloder(data), 'spotify')
        return Response(response=render_template('loading.html', id=id, type=typee), status=200, mimetype="text/html")


class youtube(Resource):

    def get(self):
        return Response(response=render_template('index.html', mode=2), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']
        id, typee = db_connection.db_insertion(
            spotify_downloader.main_yt_downloder(data), 'youtube')
        return Response(response=render_template('loading.html', id=id, type=typee), status=200, mimetype="text/html")


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


class songgs_download_yt(Resource):
    def post(self):
        data = request.json
        id = data['id']
        song_no = data['song_no']
        if song_no == 1:
            return {'message': ''}
        track = db_connection.song_name_retrevial(id, song_no)
        track_name = spotify_downloader.youtube_part(track, str(id))
        return {'message': track_name}


class download_file(Resource):

    def get(self):
        data = request.args.get('id')
        id = str(data)
        plalist_songs_name = os.listdir(f'music{id}')
        if len(plalist_songs_name) <= 1:
            return send_file(f'music{id}/{plalist_songs_name[0]}', as_attachment=True)
        spotify_downloader.creating_zip(id, plalist_songs_name)
        return send_file(f'playlist{id}.zip', as_attachment=True)


api.add_resource(Hello, '/')
api.add_resource(spotify, '/spotify')
api.add_resource(youtube, '/youtube')
api.add_resource(songgs_download, '/songgs_download')
api.add_resource(songgs_download_yt, '/songgs_download_yt')
api.add_resource(get_playlist_songs_no, '/get_playlist_songs_no')
api.add_resource(download_file, '/download_file')


# driver function
if __name__ == '__main__':

    app.run(debug=True,)
