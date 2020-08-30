import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

def login(uname):
    print("Loggin in")
    global scope 
    global username
    global spotifyObject
    scope = "playlist-modify-public user-read-playback-state user-modify-playback-state"
    # username = "arnavmenon"
    username = uname

    token = SpotifyOAuth(scope=scope, username=username)
    spotifyObject = spotipy.Spotify(auth_manager=token)

def create_playlist():
    print("Creating")
    # create playlist
    playlist_title = input("What do you want to name the playlist? ")
    # playlist_title = "h"
    playlist_description = input("Describe the playlist: ")
    # playlist_description = "h"

    spotifyObject.user_playlist_create(user=username, name=playlist_title, public=True, description=playlist_description)

    user_input = input("What song do you want to add? ('q' to exit) ")
    # user_input = "drip too hard"
    list_of_songs = []
    # list_of_songs.append("78QR3Wp35dqAhFEc2qAGjE")
    # spotify:track:78QR3Wp35dqAhFEc2qAGjE

    while user_input != "q":
        result = spotifyObject.search(q=user_input)
        list_of_songs.append(result["tracks"]["items"][0]["uri"])
        user_input = input("What song do you want to add? ('quit' to exit) ")

    # with open("data.json", "w") as write_file:
    #     json.dump(spotifyObject.user_playlists(user=username), write_file, indent=2)

    pre_playlist = spotifyObject.user_playlists(user=username)
    playlist = pre_playlist["items"][0]["id"]

    spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)


if __name__ == "__main__":
    # login()
    create_playlist()