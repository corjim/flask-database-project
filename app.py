from flask import Flask, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
import os
from markupsafe import Markup


from models import db, connect_db, Playlist, PlaylistSong, Song
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
# Please do not modify the following line on submission
# app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('SUPABASE_DB_URL'), 'postgresql:///playlist-app')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.mlcupgkougldvbyodeah:DJdatabase@2024@aws-0-us-west-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

db.drop_all()
db.create_all()


app.config['SECRET_KEY'] = "The sky is the limit"



@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)

@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get_or_404(playlist_id)

    if not playlist: 
        return flash (f' Playlist not found') 


    return render_template("playlist.html",playlist=playlist)

@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        playlist = Playlist(name=name, description=description)

        db.session.add(playlist)
        db.session.commit()

        return redirect('/playlists')
    else:
        return render_template('/new_playlist.html', form=form)

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()

    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    song = Song.query.get(song_id)

    if not song:

        return flash(f'Song not found')

    return render_template('song.html', song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        song = Song(title=title, artist=artist)

        db.session.add(song)
        db.session.commit()

        return redirect('/songs')
    else:
        return render_template('new_song.html', form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = [
    (song.id, song.title) for song in db.session.query(Song.id, Song.title)
    .filter(Song.id.notin_(curr_on_playlist))
    .all()]       

    if form.validate_on_submit():

        playlist_song = PlaylistSong(song_id=form.song.data, playlist_id=playlist_id)

        db.session.add(playlist_song)
        db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                           playlist=playlist,
                           form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 5505,
            debug=True)
