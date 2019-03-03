import spotipy, sys, os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import urllib3
import requests

my_token = os.getenv('MY_TOKEN')
username = os.getenv('USERNAME')
scope = 'user-library-read'

client_credentials_manager = SpotifyClientCredentials()
token = util.prompt_for_user_token(username, scope)
if not token:
    print('Something went wrong, exiting')
    exit(1)

sp = spotipy.Spotify(token, True, client_credentials_manager=client_credentials_manager)
user = sp.user(username)

if not sp:
    print('Something went wrong, exiting')
    exit(1)


# API call to get the current user info
# GET: 200 
def get_user(username):
    user = sp.user(username)
    return user

# GET: retrieve an artist by ID
''' TODO: make the id dynamically '''
def get_artist(choice):
    valid=['album','single','appears_on','compilation']
    song_list= []
    if choice in valid:
        artist = sp.artist_albums('3TVXtAsR1Inumwj472S9r4',album_type=choice,limit=20)
        for item in artist['items']:
            song={}
            song['name'] = item['name']
            song['release_date'] = item['release_date']
            song_list.append(song)
    else:
        artist = sp.artist_albums('3TVXtAsR1Inumwj472S9r4',album_type='album',limit=20)
        for item in artist['items']:
            song={}
            song['name'] = item['name']
            song['release_date'] = item['release_date']
            song_list.append(song)
    return song_list

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

# Gets detailed information about the current user
def get_current_user_detail():
    var=sp.me()
    return(var['display_name'])
    #return sp.me()

# gets the current users top tracks
def get_current_user_top_tracks():
    tracks = sp.current_user_top_tracks(limit=5)
    print(tracks)
    return tracks

# Get information about the current users currently playing track
def user_playlist(user=None, cap=5):
    if user == 'none':
        user = username
    playlists = sp.user_playlists(user, limit=int(cap))
    plists = {}
    plists['total'] = playlists['total']
    plists['limit'] = playlists['limit']
    p = {}
    ant = 1
    #print(playlists['items'])
    items = playlists['items']
    for item in items:
        #print(item, '\n\n')
        p['name'] = item['name']
        p['owner'] = item['owner']['display_name']
        p['id'] = item['id']
        p['total_tracks'] = item['tracks']['total']
        p['uri'] = item['uri']
        key = 'playlist_' + str(ant)
        plists[key] = p 
        ant += 1
    return plists

def DJT():
    http = urllib3.PoolManager()
    r = http.request('GET','https://api.tronalddump.io/random/quote')
    data = r.data.decode('utf-8')
    resp = json.loads(data)
    return resp['value']
    

# Retrives the current user's playing song.
def get_current_playing_song():
    # GET: /v1/me/player/recently-played
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + my_token})
    data = {}
    if r.status_code != 200:
        data['error'] = True
        data['error_code'] = r.status_code
        return data
    resp = r.json()
    data['error'] = False
    data['error_code'] = r.status_code
    #song = {"artist" : data['data']['item']['album'], "song": data['data']}
    artists = []
    for artist in resp['item']['artists']:
        artists.append(artist['name'])
    data['name'] = resp['item']['name']
    data['release_date'] = resp['item']['album']['release_date']
    data['artists'] = artists
    data['is_playing'] = resp['is_playing']
    #data['data'] = resp
    return data
