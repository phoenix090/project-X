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
    def get(self, username):
        user = {}
        spotify_user = spotify_api.get_user(username)
        if spotify_user:
            user['id'] = spotify_user['id']
            user['display_name'] = spotify_user['display_name']
            user['followers'] = spotify_user['followers']['total']
            return { 'user': user}, 200
        else:
            return {'error': 'did not find the user'}, 404

class Playlist(Resource):
    def get(self, id):
        pass

class Me(Resource):
    def get(self):
        me = spotify_api.get_current_user_detail()
        return {'me' : me}, 200

class PlayingTrack(Resource):
    def get(self):
        pass

class User_playlists(Resource):
    def get(self, username, limit):
        playlists = spotify_api.user_playlist(username, limit)
        return { 'playlists' : playlists }, 200

class User_Top_Tracks(Resource):
    def get(self):
        tracks = spotify_api.get_current_user_top_tracks()
        return {'tracks' : tracks}

api.add_resource(Home, '/')
api.add_resource(Me, '/me')
api.add_resource(User, '/user/<username>')
api.add_resource(User_playlists, '/user/<username>/playlists/<limit>')
api.add_resource(Playlist, '/playlist/<id>')
api.add_resource(User_Top_Tracks, '/tracks')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)