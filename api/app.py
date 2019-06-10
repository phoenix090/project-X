from flask import Flask
import spotify_api
from flask_restful import Resource, Api
import time

app = Flask(__name__)
api = Api(app)



''' Endpoint for home enpoint (/) '''  
class Home(Resource):
    def get(self):
        return { 'API version': '0.0.1',
                'Description': 'Simple Spotify API'}, 200

''' Endpoint to get a specific user information '''  
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

''' Endpoint for a specific playlist '''  
''' @id of the playlist in spotify '''
class Playlist(Resource):
    def get(self, id):
        pass

''' Endpoint for current user's information '''   
class Me(Resource):
    def get(self):
        data = spotify_api.get_current_user_detail()
        return {'me' : data['user']}, data['status_code']

''' Endpoint for current playing song '''   
class PlayingTrack(Resource):
    def get(self):
        resp = spotify_api.get_current_playing_song()
        return {"response" : resp}, resp['error_code']
    
''' Endpoint to get user's playslists '''   
class User_playlists(Resource):
    def get(self, username, limit):
        pass
        # playlists = spotify_api.user_playlist(username, limit)
        # return { 'playlists' : playlists }, 200

''' Endpoint to get the artist song '''        
class Get_artist_songs(Resource):
    def get(self,choice):
        pass
        # song = spotify_api.get_artist(choice)
        # return {'songs' : song}

''' Endpoint for gets the user's top tracks '''
class User_Top_Tracks(Resource):
    def get(self):
        pass
        # tracks = spotify_api.get_current_user_top_tracks()
        # return {'tracks' : tracks}

''' Endpoint for trump stuff '''
class Tronald_Dump(Resource):
    def get(self):
        trump=spotify_api.DJT()
        return {'haha_joke' : trump} 

#spotify_api.get_artist_id("0TnOYISbd1XYRBk9myaseg")
''' Endpoint for getting the all devices that the current user is using '''
class Devices(Resource):
    def get(self):
        devs = spotify_api.available_devices()
        return {'response' : devs}, devs['error_code']


''' Endpoint for playing the next song '''
class Play_next(Resource):
    def post(self):
        resp = spotify_api.play_next()
        return { 'status': resp['status_code'] }, resp['status_code']


''' Endpoint for playing the previous song '''
class Play_previous_song(Resource):
    def post(self):
        resp = spotify_api.play_previous_song()
        return { 'status': resp['status_code'] }, resp['status_code']

''' Endpoint for playing the previous song '''
class MyPlaylists(Resource):
    def get(self):
        resp = spotify_api.my_playlists()
        albums = {}
        albums['total_playlists'] = len(resp)
        albums['playlists'] = resp

        if albums['total_playlists']:
            return { 'response': albums }, 200
        return { 'Error': "Could not get playlists" }, 404

''' Pauses the users playback '''
class Pause(Resource):
    def get(self):
        resp = spotify_api.pause_song()
        return {}, resp

''' Resume son '''
class Play(Resource):
    def get(self):
        resp = spotify_api.resume_song()
        return {}, resp

''' Repeat mode'''
class Repeat(Resource):
    def get(self):
        resp = spotify_api.repeat_mode()
        return {}, resp

''' Adjust the volume '''
class Set_volume(Resource):
    def get(self, level):
        resp = spotify_api.set_volume(level)
        return {}, resp


# spotify_api.get_current_playing_song()
api.add_resource(Home, '/')
api.add_resource(Me, '/me')
api.add_resource(MyPlaylists, '/me/playlists')
api.add_resource(User, '/user/<username>')
api.add_resource(User_playlists, '/user/<username>/playlists/<limit>')
api.add_resource(Playlist, '/playlist/<id>')
#api.add_resource(User_Top_Tracks, '/tracks')
api.add_resource(Get_artist_songs, '/library/<choice>')
api.add_resource(Tronald_Dump, '/tjokes')
api.add_resource(PlayingTrack, '/current_song')
api.add_resource(Devices, '/devices')
api.add_resource(Play_next, '/next')
api.add_resource(Play_previous_song, '/previous')
api.add_resource(Pause, '/pause')
api.add_resource(Play, '/play')
api.add_resource(Set_volume, '/volume/<level>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)