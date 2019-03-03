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
        resp = spotify_api.get_current_playing_song()
        if resp['error']:
            return {"response" : resp}, resp['error_code']
        else:
            return {"response" : resp}, resp['error_code']

class User_playlists(Resource):
    def get(self, username, limit):
        playlists = spotify_api.user_playlist(username, limit)
        return { 'playlists' : playlists }, 200
class Get_artist_songs(Resource):
    def get(self,choice):
        song = spotify_api.get_artist(choice)
        return {'songs' : song}

class User_Top_Tracks(Resource):
    def get(self):
        tracks = spotify_api.get_current_user_top_tracks()
        return {'tracks' : tracks}

class Tronald_Dump(Resource):
    def get(self):
        trump=spotify_api.DJT()
        return {'haha_joke' : trump} 


# spotify_api.get_current_playing_song()
api.add_resource(Home, '/')
api.add_resource(Me, '/me')
api.add_resource(User, '/user/<username>')
api.add_resource(User_playlists, '/user/<username>/playlists/<limit>')
api.add_resource(Playlist, '/playlist/<id>')
#api.add_resource(User_Top_Tracks, '/tracks')
api.add_resource(Get_artist_songs, '/library/<choice>')
api.add_resource(Tronald_Dump, '/tjokes')
api.add_resource(PlayingTrack, '/current_song')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)