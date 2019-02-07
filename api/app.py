from flask import Flask
import spotify_api
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return { 'API version': '0.0.1',
                'Description': 'Simple Spotify API'}, 200

class User(Resource):
    def get(self):
        user = {}
        spotify_user = spotify_api.get_user('hamse-90')
        if spotify_user:
            user['id'] = spotify_user['id']
            user['display_name'] = spotify_user['display_name']
            user['followers'] = spotify_user['followers']['total']
            return { 'user': user}, 200
        else:
            return {'error': 'did not find the user'}, 404

api.add_resource(Home, '/')
api.add_resource(User, '/user/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)