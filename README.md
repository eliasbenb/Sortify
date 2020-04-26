
<a href="#"><h3 align="center"><img src="https://i.ibb.co/V9xTH3D/Sortify-Header.png" width="600px"></h3></a>
<p align="center">
  <a href="https://github.com/eliasbenb/Sortify/releases/latest"><img src="https://img.shields.io/github/v/release/eliasbenb/Sortify?color=%231DB954&style=for-the-badge"></a>
</p>
<p align="center">
  <a href="https://eliasbenb.github.io"><img src="https://i.ibb.co/6mG3jFz/Produced-by-eliasbenb.png" width="180"></a>
</p>

# What is this repo?
Sortify is a Python app built with the Flask framework. It uses the [Spotipy](https://github.com/plamere/spotipy) API to allow you to view and sort your Spotify playlists to your heart's content. I hosted the app on [Heroku](https://eliasbenb-sortify.herokuapp.com/).


## Features supported:
- Supported sorting options:
	- Alphabetically (A-Z)
	- Alphabetically (Z-A)
	- Release Date (Chronological)
	- Release Date (Non Chronological)
	- Added Date
- View playlist tracks in a table
- Heroku deploy ready

## To do list:
- Add support to sort playlists of more than 100 tracks
- Add support to sort other people's playlists
- Add option to sort playlist into new playlist

# Installation
### Prerequisites:
- A server, could be your own computer or [Heroku](https://heroku.com); this repository is Heroku ready
- [Python](https://www.python.org/downloads/) 3.8 or above
- A [Spotify](https://developer.spotify.com/dashboard/applications) app

### Part 1 (Spotify API):
- First you need to setup a Spotify API app. To do this go to the [Spotify Developer's Dashboard](https://developer.spotify.com/)
- Create an app
- Name the app anything and describe it as anything. But set it as a *Website*
- On the app's page click *Edit Settings* and under *Redirect URIs* add this: `http://127.0.0.1:5000/callback`
- If your app is not locally hosted than make the Redirect URI something like this `https://yourwebsite.com/callback`
- Finally exit back onto the main app's page and copy down the *Client ID* and *Client Secret*, you will need these in the next step

### Part 2 (The App):
- Now it's time to make the app. First clone this repository in a command line using `git clone https://github.com/eliasbenb/Sortify.git`
- CD into the directory with `cd Sortify`
- Open `app.py` with a text editor and change the following variables:
	- `app.secret_key` to any string e.g. "string123"
	- `SPOTIFY_CLIENT_ID` to the *Client ID* you got from [Step 1](#Part-1-Spotify-API)
	- `SPOTIFY_CLIENT_SECRET` to the *Client Secret* you got from [Step 1](#Part-1-Spotify-API)
	- `REDIRECT_URI` to whatever you set your *Redirect URI* to in [Step 1](#Part-1-Spotify-API)
- If you are setting this up for a public website like I am I would recommend using Environment Variables to set the above variables
- Now your app is ready to be used, to start the app just enter this in a command line `flask run`

# Usage:
### Home Page:
- The home page contains Sortify information
- And it contains a 'Login' button, clicking it will lead to the Spotify authentication page

![Home Page](https://user-images.githubusercontent.com/54410649/80308198-97f31080-87de-11ea-99f5-8dd0dc5b8106.png)
### Login Page:
- After successfully authenticating your Spotify account, you will receive a success message

![Login Page](https://user-images.githubusercontent.com/54410649/80308225-c244ce00-87de-11ea-8e39-6c718ea49b7d.png)
### Playlists Page:
- After scrolling down on the playlists page you will see all your playlists's images, clicking one will open that playlist's page

![Playlists Page](https://user-images.githubusercontent.com/54410649/80308226-c375fb00-87de-11ea-9f5d-bee2dbd56c64.png)
### Playlist Page:
- The playlist page contains a table which displays all the playlist's tracks and its information
- Below that there are a group of buttons which allow you to sort the playlist:
	- Alphabetically (A-Z)
	- Alphabetically (Z-A)
	- Release Date (Chronological)
	- Release Date (Non Chronological)
	- Added Date

![Playlist Page](https://user-images.githubusercontent.com/54410649/80308227-c4a72800-87de-11ea-8707-625b13eecff4.png)
