from email import message
from flask import Flask, Response, jsonify, request, render_template, send_file
from flask_restful import Resource, Api
import spotify_downloader
import os
import glob
import threading
app = Flask(__name__)

api = Api(app)


def deleting():
    if not os.path.exists('music'):
        os.makedirs('music')

    for file in glob.glob("music/*"):
        os.remove(file)
    try:
        os.remove("plalylist.zip")
    except:
        pass


class Hello(Resource):

    def get(self):
        threading.Thread(target=deleting).start()
        return Response(response=render_template('index.html'), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']     # status code
        text = spotify_downloader.track_record(data)
        return Response(response=render_template('loading.html', message=text), status=200, mimetype="text/html")


class get_playlist_songs_no(Resource):

    def get(self):

        return {'songs_number': len(spotify_downloader.tracks)+1}


class songgs_download(Resource):
    def get(self):

        print(len(spotify_downloader.tracks))
        if not spotify_downloader.tracks:
            return {'message': ''}
        track_name = spotify_downloader.spoti_tube()
        return {'message': track_name}


class download_file(Resource):

    def get(self):
        spotify_downloader.creating_zip()
        return send_file('plalylist.zip', as_attachment=True)


api.add_resource(Hello, '/')
api.add_resource(songgs_download, '/songgs_download')
api.add_resource(get_playlist_songs_no, '/get_playlist_songs_no')
api.add_resource(download_file, '/download_file')


# driver function
if __name__ == '__main__':

    app.run(debug=True,)
