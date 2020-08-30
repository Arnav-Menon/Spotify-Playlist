from flask import Flask, render_template, flash, request, redirect, session
from flask.helpers import url_for
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import spotipy
from json import JSONDecodeError
import os

app = Flask(__name__)
app.secret_key = "SDHFJKSDFHUIEF"
app.permanent_session_lifetime = timedelta(minutes=1)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

scope = "playlist-modify-public user-top-read user-read-playback-state"

db = SQLAlchemy(app)

class playlist(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

@app.route("/")
@app.route("/home")
def home_page():
    global username
    global spotifyObject
    username = "arnavmenon"
    try:
        token = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username)
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username)

    spotifyObject = spotipy.Spotify(auth_manager=token)
    user = spotifyObject.current_user()
    display_name = user["display_name"]
    flash("Welcome to Spotify on the Web, " + str(display_name))
    return render_template("home.html")

# def home_page():
#     global username
#     global token
#     global spotifyObject
#     username = "arnavmenon"
#     token = spotipy.oauth2.SpotifyOAuth(scope=scope, username=username)

#     if token:
#         spotifyObject = spotipy.Spotify(auth_manager=token)
#         flash("Welcome to Spotify on the Web")
#         return render_template("home.html")
#     else:
#         return "<h5>Can't log you in</h5>"

# @app.route("/next")
# def next():
#     next_song()
#     return render_template("home.html")

# @app.route("/login")
# def login():
    # login()

# @app.route("/logout")
# def logout():

@app.route("/playlists")
def display_playlists():
    global spotifyObject

    p = spotifyObject.current_user_playlists()
    playlists = []

    for x in p["items"]:
        playlists.append(x["name"])
    
    flash("Your Playlists")
    return render_template("display.html",playlists=playlists)

# "GET" must be specified if methods in declared, otherwise it is automatic
@app.route("/create_playlist", methods=["GET", "POST"])
def create_playlist():
    if request.method == "POST":
        global spotifyObject
        session.permanent = True
        title = request.form["title"]
        description = request.form["desc"]
        length = request.form["size"]
        term = request.form["time"]
        # these dict keys can be named anything
        session["t"] = title
        session["d"] = description
        session["l"] = length
        session["r"] = term
        if title != "" or description != "":
            # flash("Playlist Title and Description Saved")
            plst = playlist(title, description)
            db.session.add(plst)
            db.session.commit()
            return redirect(url_for("generate_playlist"))
        else:
            flash("Please fill in all boxes")
            return redirect(request.url)

    return render_template("playlist.html")

@app.route("/generate")
def generate_playlist():
    if "t" in session:
        global spotifyObject
        playlist_title = session["t"]
        playlist_description = session["d"]
        limit = int(session["l"])
        time_range = session["r"]
        list_of_songs = []

        spotifyObject.user_playlist_create(user=username, name=playlist_title, description=playlist_description)

        top_tracks = spotifyObject.current_user_top_tracks(limit=limit,time_range=time_range)

        for i in range(0, limit):
            list_of_songs.append(top_tracks["items"][i]["id"])

        pre_playlist = spotifyObject.user_playlists(user=username)
        playlist = pre_playlist["items"][0]["id"]

        spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)

        flash("Playlist Created")
        return redirect(url_for("home_page"))
    else:
        return redirect(url_for("create_playlist"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)