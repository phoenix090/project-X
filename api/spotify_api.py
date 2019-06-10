import spotipy, sys, os
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import urllib3
import requests
import time

TOKEN = os.getenv('TOKEN')
USERNAME = os.getenv('USERNAME')
SCOPE = '''user-read-recently-played user-top-read user-library-read playlist-read-private playlist-read-collaborative
        user-read-email user-read-birthdate user-read-private user-read-playback-state user-modify-playback-state 
        user-read-currently-playing app-remote-control streaming user-follow-read'''

client_credentials_manager = SpotifyClientCredentials()
TOKEN = util.prompt_for_user_token(USERNAME, SCOPE)
#print(TOKEN)
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REFRESH_TOKEN = ""
CASHE_PATH = os.getenv('CASHE_PATH')

# if not TOKEN:
#     print('Something went wrong, exiting')
#     exit(1)
#sp = spotipy.Spotify(TOKEN, True, client_credentials_manager=client_credentials_manager)
OAUTH = spotipy.oauth2.SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SCOPE, CASHE_PATH)
# try:
#     with open('.cache-' + USERNAME) as f:
#         content = f.read()
#         token_info = json.loads(content)
    
#     print(token_info)
#     if OAUTH._is_token_expired(token_info):
#         TOKEN = OAUTH.get_access_token(TOKEN)
#         print(TOKEN)
#         OAUTH._save_token_info(TOKEN)
#         print(TOKEN)
#     else:
#         print("has not expired..")
# except IOError as e:
#     print("Noe gikk galt: ", e)

#AUTH_URL = OAUTH.get_authorize_url()
#TOKEN_DETAILS = requests.get(AUTH_URL)
# if TOKEN_DETAILS.status_code == 200:
    # resp = TOKEN_DETAILS.json()
    # print(resp)


# user = sp.user(USERNAME)

# if not sp:
#     print('Something went wrong, exiting')
#     exit(1)

def get_artist_id(id):
    r = requests.get(' https://api.spotify.com/v1/artists/'+id, headers = {'Authorization':'Bearer '+ TOKEN})
    dat = r.json()
    alist = []
    alist.append(dat['name'])
    alist.append(dat['genres'])
    print(dat['name'],dat['genres'])
    return alist

# API call to get the current user info
# GET: 200 
def get_user(uname):
    url = 'https://api.spotify.com/v1/users/' + uname
    params = {'Content-Type' : 'application/json', 'Authorization': 'Bearer ' + TOKEN}
    data = {}

    r = requests.get(url, headers=params)
    if r.status_code == 401:
        if refresh_token():
            get_user(uname)
    
    return r.json()

# GET: retrieve an artist by ID
''' TODO: make the id dynamically '''
def get_artist(choice):
    pass
#     valid=['album','single','appears_on','compilation']
#     song_list= []
#     if choice in valid:
#         artist = sp.artist_albums('3TVXtAsR1Inumwj472S9r4',album_type=choice,limit=20)
#         for item in artist['items']:
#             song={}
#             song['name'] = item['name']
#             song['release_date'] = item['release_date']
#             song_list.append(song)
#     else:
#         artist = sp.artist_albums('3TVXtAsR1Inumwj472S9r4',album_type='album',limit=20)
#         for item in artist['items']:
#             song={}
#             song['name'] = item['name']
#             song['release_date'] = item['release_date']
#             song_list.append(song)
#     return song_list

# GET: gets an artist's top tracks, use COUNTY to limit the request
def get_artist_top_tracks():
    pass
    # top_tracks = sp.artist_top_tracks('2YZyLoL8N0Wb9xBt1NhZWg')
    # for tracks in top_tracks['tracks']:
    #     for album in tracks:
    #         if album == 'album':
    #             #print('name: ', tracks['album']['name'], '\n')
    #             #print('total tracks: ', tracks['album']['total_tracks'], '\n')
    #             #print('release date: ', tracks['album']['release_date'], '\n')
    #             print('key: ', tracks['album'], '\n')   

# Gets detailed information about the current user
def get_current_user_detail():
    url = 'https://api.spotify.com/v1/me'
    params = {'Content-Type' : 'application/json', 'Authorization': 'Bearer ' + TOKEN}
    data = {}

    r = requests.get(url, headers=params)
    if r.status_code == 401:
        if refresh_token():
            get_current_user_detail()
    
    resp = r.json()
    user = {}
    data['status_code'] = r.status_code
    user['display_name'] = resp['display_name']
    user['birthdate'] = resp['birthdate']
    user['country'] = resp['country']
    user['product'] = resp['product']
    data['user'] = user
    return data

# gets the current users playlists
def my_playlists():
    url = 'https://api.spotify.com/v1/me/playlists'
    params = {'Content-Type' : 'application/json', 'Authorization': 'Bearer ' + TOKEN}

    r = requests.get(url, headers=params)
    if r.status_code == 401:
        if refresh_token():
            get_current_user_detail()
            return

    resp = r.json()
    data = []
    print(r.status_code)
    if r.status_code is not 200:
        return data
    ant = 0
    for item in resp['items']:
        album = {}
        if ant == 10:
            data.append('%')
            print("burde appende")
        album['name'] = item['name']
        album['total_tracks'] = item['tracks']['total']
        data.append(album)
        ant = ant + 1
    return data

# Get information about the current users currently playing track
def user_playlist(user=None, cap=5):
    pass
    

def DJT():
    http = urllib3.PoolManager()
    r = http.request('GET','https://api.tronalddump.io/random/quote')
    data = r.data.decode('utf-8')
    resp = json.loads(data)
    return resp['value']
    
''' Retrives the current user's playing song. '''
def get_current_playing_song():
    r = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={'Authorization': 'Bearer ' + TOKEN})
    data = {}
    data['error_code'] = r.status_code
    if r.status_code == 401:
        if refresh_token():
            get_current_playing_song()

    if r.status_code != 200:
        return data

    resp = r.json()
    artists = []
    for artist in resp['item']['artists']:
        artists.append(artist['name'])

    data['name'] = resp['item']['name']
    data['release_date'] = resp['item']['album']['release_date']
    data['artists'] = artists
    data['is_playing'] = resp['is_playing']
    return data


''' GET: gets a User's Available Devices '''
def available_devices():
    data = {}
    r = requests.get('https://api.spotify.com/v1/me/player/devices', headers={'Authorization': 'Bearer ' + TOKEN})
    resp = r.json()

    ''' Checking for bad response code '''
    data['error_code'] = r.status_code
    if r.status_code == 401:
        if refresh_token():
            available_devices()

    if r.status_code != 200:
        return data

    devices = []
    for device in resp['devices']:
        devices.append(device)
    
    data['devices'] = devices
    return data

''' POST: plays the next song'''
def play_next():
    data = {}
    params = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ TOKEN}
    r = requests.post('https://api.spotify.com/v1/me/player/next', headers=params)
    if r.status_code == 401:
        if refresh_token():
            play_next()

    data['status_code'] = r.status_code
    return data

'''POST: plays the previous song '''
def play_previous_song():
    data = {}
    params = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ TOKEN}
    r = requests.post('https://api.spotify.com/v1/me/player/previous', headers=params)

    if r.status_code == 401:
        if refresh_token():
            play_previous_song()
        
    data['status_code'] = r.status_code
    return data

''' Checks if the TOKEN has expired and refreshes if so '''
def refresh_token():
    print(time.time())
    with open('.cache-' + USERNAME) as f:
        content = f.read()
        token_info = json.loads(content)
    if token_info is None:
        print('could not find token_info from file')
        return False
    refresh_token = token_info['refresh_token']
    new_token_info = OAUTH.refresh_access_token(refresh_token)
    print(new_token_info)
    if new_token_info is None:
        print('could not refresh access token, got: ', new_token_info)
        return False       
    TOKEN = new_token_info['access_token']
    return True


def pause_song():
    # https://api.spotify.com/v1/me/player/pause
    req = requests.put('https://api.spotify.com/v1/me/player/pause', headers= {'Authorization': 'Bearer ' + TOKEN})
    if req.status_code == 403:
        if refresh_token():
            resume_song()
    return req.status_code

def resume_song():
    # https://api.spotify.com/v1/me/player/play
    req = requests.put('https://api.spotify.com/v1/me/player/play', headers= {'Authorization': 'Bearer ' + TOKEN})
    if req.status_code == 403:
        if refresh_token():
            resume_song()
    return req.status_code

def repeat_mode():
    #https://api.spotify.com/v1/me/player/repeat
    req = requests.put('https://api.spotify.com/v1/me/player/repeat', headers= {'Authorization': 'Bearer ' + TOKEN})
    if req.status_code == 403:
        if refresh_token():
            repeat_mode()
    return req.status_code

def set_volume(percent):
    #https://api.spotify.com/v1/me/player/repeat

    req = requests.put('https://api.spotify.com/v1/me/player/volume', headers= {'Authorization': 'Bearer ' + TOKEN}, params={'volume_percent' : int(percent)})
    if req.status_code == 403:
        if refresh_token():
            set_volume(percent)
    return req.status_code