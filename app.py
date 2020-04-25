from flask import Flask, url_for, render_template
from datetime import datetime
import spotipy.util as util
import spotipy, os

def get_tracks(spotipy_obj, username, playlist_ids):
    results = spotipy_obj.user_playlist(username, playlist_ids, fields="tracks, next")
    temp_tracks = results["tracks"]

    original_tracks = temp_tracks["items"]

    while temp_tracks["next"]:
        temp_tracks = spotipy_obj.next(temp_tracks)

        original_tracks.extend(temp_tracks["items"])

    return original_tracks

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login')
def login_page():
    spotipy_redirect_uri = "http://localhost:8080/callback/"
    scope = 'user-read-email user-read-private playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'
    spotipy_client_id = os.getenv('SPOTIPY_CLIENT_ID')
    spotipy_client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
    token = util.prompt_for_user_token("spotify", scope, spotipy_client_id, spotipy_client_secret, spotipy_redirect_uri)
    if token:
        global sp
        global username
        sp = spotipy.Spotify(auth=token)
        username = sp.current_user()['id']
    return render_template('login.html')

@app.route('/playlists')
def playlists_page():
    if 'sp' not in globals():
        login_page()
    elif 'sp' in globals():
        global playlists_soup
        playlists_soup = sp.current_user_playlists()
        return render_template('playlists.html', playlists_soup = playlists_soup)

@app.route('/playlists/<int:index>')
def playlist_page(index):
    playlist = playlists_soup['items'][index-1]
    playlist_name = playlist['name']
    playlist_id = playlist['id']
    global original_tracks
    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))
    results = sp.playlist(playlist['id'],
        fields="tracks,next")
    tracks = results['tracks']
    return render_template('playlist.html', playlist = playlist, playlist_name = playlist_name, playlist_id = playlist_id, playlists_soup = playlists_soup, tracks = tracks, index = index)

@app.route('/playlists/<int:index>/added_at')
def sort_by_added_at(index):
    playlist_name = playlists_soup['items'][index-1]['name']
    playlist_id = playlists_soup['items'][index-1]['id']
    sorted_tracks = sorted(original_tracks,
                    key=lambda k: datetime.strptime(k["added_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    return render_template('sorted.html', playlist_name = playlist_name, index = index)

@app.route('/playlists/<int:index>/alphabetical-az')
def sort_by_alphabetical_az(index):
    playlist_name = playlists_soup['items'][index-1]['name']
    playlist_id = playlists_soup['items'][index-1]['id']
    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']["name"], reverse=False)
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    return render_template('sorted.html', playlist_name = playlist_name, index = index)

@app.route('/playlists/<int:index>/alphabetical-za')
def sort_by_alphabetical_za(index):
    playlist_name = playlists_soup['items'][index-1]['name']
    playlist_id = playlists_soup['items'][index-1]['id']
    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']["name"], reverse=True)
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    return render_template('sorted.html', playlist_name = playlist_name, index = index)

@app.route('/playlists/<int:index>/release_date-chronological')
def sort_by_release_date_chronological(index):
    playlist_name = playlists_soup['items'][index-1]['name']
    playlist_id = playlists_soup['items'][index-1]['id']
    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']['album']['release_date'], reverse=True)
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    return render_template('sorted.html', playlist_name = playlist_name, index = index)

@app.route('/playlists/<int:index>/release_date-non_chronological')
def sort_by_release_date_non_chronological(index):
    playlist_name = playlists_soup['items'][index-1]['name']
    playlist_id = playlists_soup['items'][index-1]['id']
    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']['album']['release_date'], reverse=False)
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    return render_template('sorted.html', playlist_name = playlist_name, index = index)

if __name__ == '__main__':
    app.run(debug=True, port=37145)
