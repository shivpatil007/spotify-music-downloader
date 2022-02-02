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
        songs_number = 4  # spotify_downloader.get_song_number(data)
        spotify_downloader.spoti_tube(data)
        return Response(response=render_template('download.html'), status=200, mimetype="text/html")


class download_file(Resource):

    def get(self):
        return send_file('plalylist.zip', as_attachment=True)


api.add_resource(Hello, '/')
api.add_resource(download_file, '/download_file')


# driver function
if __name__ == '__main__':

    app.run(debug=False,)
