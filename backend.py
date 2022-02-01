from flask import Flask, Response, jsonify, request, render_template
from flask_restful import Resource, Api
import spotify_downloader
import time
app = Flask(__name__)

api = Api(app)


class Hello(Resource):

    def get(self):

        return Response(response=render_template('index.html', box=True), status=200, mimetype="text/html")

    def post(self):
        data = request.form['to-dow-link']     # status code
        songs_number = 4  # spotify_downloader.get_song_number(data)
        print("wating for download")
        time.sleep(10)
        print("downloading")
        return Response(response=render_template('index.html', songs_number=songs_number), status=200, mimetype="text/html")


class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})


api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')


# driver function
if __name__ == '__main__':

    app.run(debug=True)
