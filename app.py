from flask import Flask, render_template, redirect, request, session, make_response, url_for
from datetime import datetime
import os, requests, spotipy, sys
import spotipy.util as util

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

def get_tracks(spotipy_obj, username, playlist_id):
    results = spotipy_obj.user_playlist(username, playlist_id, fields="tracks, next")
    temp_tracks = results["tracks"]

    original_tracks = temp_tracks["items"]

    while temp_tracks["next"]:
        temp_tracks = spotipy_obj.next(temp_tracks)

        original_tracks.extend(temp_tracks["items"])

    return original_tracks

def replace_tracks(sorted_tracks, sp, playlist_id, username):
    track_ids = []
    for sorted_track in sorted_tracks:
        track_ids.append(sorted_track['track']['id'])
    
    if len(track_ids) > 100:
        chunks = [track_ids[x:x+100] for x in range(0, len(track_ids), 100)]
        sp.user_playlist_replace_tracks(username, playlist_id, "")
        for track_ids in chunks:
            sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    else:
        sp.user_playlist_replace_tracks(username, playlist_id, track_ids)
    

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SCOPE = 'playlist-read-collaborative,playlist-read-private,playlist-modify-public,playlist-modify-private'
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
API_BASE = 'https://accounts.spotify.com'
SHOW_DIALOG = True

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/login")
def login_page():
    auth_url = f'{API_BASE}/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
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
    session["token"] = res_body.get("access_token")
    
    return redirect("login_success")

@app.route("/login_success")
def login_success_page():
    return render_template("login_success.html")

@app.route('/playlists')
def playlists_page():
    try:
        sp = spotipy.Spotify(auth=session['token'])
        playlists_soup = sp.current_user_playlists()
        return render_template('playlists.html', playlists_soup = playlists_soup)
    except:
        return redirect("login")

@app.route('/not_your_playlist')
def not_your_playlist_page():
    return render_template('not_your_playlist.html')

@app.route('/playlists/<int:index>')
def playlist_page(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    if playlist['owner']['id'] != username:
        return redirect (url_for("not_your_playlist_page"))
    
    else:
        original_tracks = []
        original_tracks.extend(get_tracks(sp, username, playlist_id))
        results = sp.playlist(playlist['id'],
            fields="tracks,next")
        tracks = results['tracks']
        return render_template('playlist.html', playlist = playlist, tracks = tracks, index = index)

@app.route('/playlists/<int:index>/alphabetical-az')
def sort_by_alphabetical_az(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))

    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']["name"], reverse=False)
    replace_tracks(sorted_tracks, sp, playlist_id, username)
    return render_template('sorted.html', playlist = playlist, index = index)

@app.route('/playlists/<int:index>/alphabetical-za')
def sort_by_alphabetical_za(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))

    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']["name"], reverse=True)
    replace_tracks(sorted_tracks, sp, playlist_id, username)
    return render_template('sorted.html', playlist = playlist, index = index)

@app.route('/playlists/<int:index>/release_date-chronological')
def sort_by_release_date_chronological(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))

    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']['album']['release_date'], reverse=True)
    replace_tracks(sorted_tracks, sp, playlist_id, username)
    return render_template('sorted.html', playlist = playlist, index = index)

@app.route('/playlists/<int:index>/release_date-non_chronological')
def sort_by_release_date_non_chronological(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))

    sorted_tracks = sorted(original_tracks,
                    key=lambda k: k['track']['album']['release_date'], reverse=False)
    replace_tracks(sorted_tracks, sp, playlist_id, username)
    return render_template('sorted.html', playlist = playlist, index = index)

@app.route('/playlists/<int:index>/added_at')
def sort_by_added_at(index):
    sp = spotipy.Spotify(auth=session['token'])
    username = sp.current_user()['id']
    playlists_soup = sp.current_user_playlists()
    playlist = playlists_soup['items'][index-1]
    playlist_id = playlist['id']

    original_tracks = []
    original_tracks.extend(get_tracks(sp, username, playlist_id))

    sorted_tracks = sorted(original_tracks,
                    key=lambda k: datetime.strptime(k["added_at"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
    replace_tracks(sorted_tracks, sp, playlist_id, username)
    return render_template('sorted.html', playlist = playlist, index = index)

if __name__ == "__main__":
    app.run()