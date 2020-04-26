from flask import Flask, render_template, redirect, request, session, make_response,session,redirect
from datetime import datetime
import os, requests, spotipy
import spotipy.util as util

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

def get_tracks(spotipy_obj, username, playlist_ids):
    results = spotipy_obj.user_playlist(username, playlist_ids, fields="tracks, next")
    temp_tracks = results["tracks"]

    original_tracks = temp_tracks["items"]

    while temp_tracks["next"]:
        temp_tracks = spotipy_obj.next(temp_tracks)

        original_tracks.extend(temp_tracks["items"])

    return original_tracks

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SCOPE = 'playlist-modify-private,playlist-modify-public,user-top-read'
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
API_BASE = 'https://accounts.spotify.com'
SHOW_DIALOG = True

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/login")
def login_page():
    auth_url = f'{API_BASE}/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)

@app.route("/callback")
def callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":SPOTIFY_REDIRECT_URI,
        "client_id":SPOTIFY_CLIENT_ID,
        "client_secret":SPOTIFY_CLIENT_SECRET
        })

    res_body = res.json()
    print(res.json())
    session["toke"] = res_body.get("access_token")

    global sp
    global username
    sp = spotipy.Spotify(auth=session['toke'])
    username = sp.current_user()['id']

    return redirect("login_success")

@app.route("/login_success")
def login_success_page():
    return render_template("login_success.html")

@app.route('/playlists')
def playlists_page():
    try:
        print(sp)
        global playlists_soup
        playlists_soup = sp.current_user_playlists()
        return render_template('playlists.html', playlists_soup = playlists_soup)
    except:
        return redirect("login")

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
    for track in tracks['items']:
        print(track['added_at'])
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

if __name__ == "__main__":
    app.run()
