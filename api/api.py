from flask import Flask, request, jsonify
import spotify_api

app = Flask(__name__)


@app.route('/user/<username>', methods=['GET'])
def get_user(username):
        user = {}
        spotify_user = spotify_api.get_user(username)
        if spotify_user:
            user['id'] = spotify_user['id']
            user['display_name'] = spotify_user['display_name']
            user['followers'] = spotify_user['followers']['total']
            return jsonify({ 'user': user}), 200
        else:
            return jsonify({'error': 'did not find the user'}), 404


#api.add_resource(Spotify_API, '/spotify/user/<username>', endpoint='get_user')

if __name__ == '__main__':
    app.run(debug=True)