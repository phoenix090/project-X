import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# API call to get the current user info
# GET: 200 
def get_user(username):
    user = sp.user(username)
    return user

# GET: retrieve an artist by ID
def get_artist():
    ''' TODO: make the id dynamically '''
    artist = sp.artist('7dGJo4pcD2V6oG8kP0tJRR')
    print(artist)

# GET: gets an artist's top tracks, use COUNTY to limit the request
def get_artist_top_tracks():
    top_tracks = sp.artist_top_tracks('2YZyLoL8N0Wb9xBt1NhZWg')
    for tracks in top_tracks['tracks']:
        for album in tracks:
            if album == 'album':
                #print('name: ', tracks['album']['name'], '\n')
                #print('total tracks: ', tracks['album']['total_tracks'], '\n')
                #print('release date: ', tracks['album']['release_date'], '\n')
                print('key: ', tracks['album'], '\n')   

