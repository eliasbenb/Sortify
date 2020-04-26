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

## To do list:
- Add support to sort playlists of more than 100 tracks
- Add support to sort other people's playlists
- Add option to sort playlist into new playlist

# Installation
- To install Sortify either clone the repositry using `git clone https://github.com/eliasbenb/Sortify` or download the latest release from [here](https://github.com/eliasbenb/Sortify/releases)
- Then install the requirements using `pip install -r requirements.txt`
- Then run the Flask app using `flask run -p 37145` or you can run `app.py`

# Usage:
### Home Page:
- The home page contains Sortify information
- And it contains a 'Login' button, clicking it will lead to the Spotify authentication page

![Home Page](https://user-images.githubusercontent.com/54410649/80301627-28692b00-87b6-11ea-9297-b235a9cc7f61.PNG)
### Login Page:
- After successfully authenticating your Spotify account, you will receive a success message
- You will not need to reauthenticate your Spotify account, as the authentication is cached in the Sortify directory in a file named `.cache-spotify`

![Login Page](https://user-images.githubusercontent.com/54410649/80301630-299a5800-87b6-11ea-871c-26563b8a16b1.PNG)
### Playlists Page:
- After scrolling down on the playlists page you will see all your playlists's images, clicking one will open that playlist's page

![Playlists Page](https://user-images.githubusercontent.com/54410649/80301631-2a32ee80-87b6-11ea-8286-5bfed445dfef.PNG)
### Playlist Page:
- The playlist page contains a table which displays all the playlist's tracks and its information
- Below that there are a group of buttons which allow you to sort the playlist:
	- Alphabetically (A-Z)
	- Alphabetically (Z-A)
	- Release Date (Chronological)
	- Release Date (Non Chronological)
	- Added Date

![Playlist Page](https://user-images.githubusercontent.com/54410649/80301632-2acb8500-87b6-11ea-8b8b-d286767000c1.PNG)
