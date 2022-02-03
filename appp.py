
import os
import psycopg2
import config
from flask import Flask, Response,  request, render_template, send_file
from flask_restful import Resource, Api
import spotify_downloader
import threading
import imp_functions
import urllib.parse
app = Flask(__name__)

api = Api(app)
result = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))

conn = psycopg2.connect(
    host=result.hostname,
    database=result.path[1:],
    user=result.username,
    password=result.password

)
cursor = conn.cursor()


class Hello(Resource):

    def get(self):
        return Response(response=render_template('index.html'), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']
        tracks = spotify_downloader.track_record(data)
        unique = imp_functions.random_string(5)
        cursor.execute(
            "INSERT INTO songs_name (folder,songs) VALUES (%s,%s)", (unique, tracks))
        conn.commit()
        cursor.execute(
            "SELECT id FROM songs_name WHERE folder = %s", (unique,))
        id = cursor.fetchone()[0]
        print(id)
        threading.Thread(target=imp_functions.create_directory,
                         args=([id])).start()
        threading.Thread(target=imp_functions.deleting,
                         args=([id-1])).start()
        return Response(response=render_template('loading.html', id=id), status=200, mimetype="text/html")


class get_playlist_songs_no(Resource):
    def post(self):
        data = request.json
        id = data['id']
        print('get_playlist_songs_no->'+str(data))
        cursor.execute(
            "SELECT songs FROM songs_name WHERE id = %s", (id,))
        tracks = cursor.fetchall()[0][0][1:-1].split(',')
        return {'songs_number': len(tracks)+1}


class songgs_download(Resource):
    def post(self):
        data = request.json
        id = data['id']
        song_no = data['song_no']

        print('songgs_download->id='+str(id))
        print('songgs_download->'+str(song_no))
        if song_no == 1:
            return {'message': ''}
        cursor.execute(
            "SELECT songs FROM songs_name WHERE id = %s", (id,))
        track = cursor.fetchall()[0][0][1:-1].split(',')[song_no-2]

        track_name = spotify_downloader.spoti_tube(track, str(id))
        return {'message': track_name}


class download_file(Resource):

    def get(self):
        data = request.args.get('id')
        id = str(data)
        spotify_downloader.creating_zip(id)
        return send_file('playlist'+id+'.zip', as_attachment=True)


api.add_resource(Hello, '/')
api.add_resource(songgs_download, '/songgs_download')
api.add_resource(get_playlist_songs_no, '/get_playlist_songs_no')
api.add_resource(download_file, '/download_file')


# driver function
if __name__ == '__main__':

    app.run(debug=True,)
