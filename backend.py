from flask import Flask, Response, jsonify, request, render_template
from flask_restful import Resource, Api
from spotify_downloader import spoti_tube

app = Flask(__name__)

api = Api(app)


class Hello(Resource):

    def get(self):

        return Response(response=render_template('index.html'), status=200, mimetype="text/html")

    def post(self):

        data = request.form['to-dow-link']     # status code
        print(data)


class Square(Resource):

    def get(self, num):

        return jsonify({'square': num**2})


api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')


# driver function
if __name__ == '__main__':

    app.run(debug=True)
