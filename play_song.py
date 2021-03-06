import spotipy
from spotipy.oauth2 import SpotifyOAuth
from create_playlist import create_playlist

scope = "playlist-modify-public user-read-playback-state user-modify-playback-state user-top-read"
username = "arnavmenon"

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

device = spotifyObject.devices()

device = spotifyObject.current_playback()
d = ""
# replace empty quotes with proper device name
while d != "":
    if device["device"]["name"] == "":
        d = device["device"]["id"]
        break

def play_pause():
    if device["is_playing"] == True:
        spotifyObject.pause_playback(device_id=d)
    else:
        spotifyObject.start_playback(device_id=d)


def next_song():
    spotifyObject.next_track(device_id=d)

if __name__ == "__main__":
    play_pause()
    next_song()

    # create_playlist()