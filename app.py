from flask import Flask, redirect, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
import os
from markupsafe import Markup


from models import db, connect_db, Playlist, PlaylistSong, Song
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
# Please do not modify the following line on submission
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)

db.drop_all()
db.create_all()


app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"


a = Playlist(name="Jazz", description='Groove for days')
b = Playlist(name="Bluez", description='Night jolly')
c = Playlist(name="Pop", description='Mood setter')
d = Playlist(name="Afro", description='Dance the sweats off')

db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.add(d)
db.session.commit()


y = Song(title= 'we could be heros',artist='Claire')
u = Song(title= 'dancing with father',artist='Luther V')
t = Song(title= 'Best night',artist='Usher')
q = Song(title= 'Hit em',artist='2Pac')
y = Song(title= 'yeye',artist='Burna Boy')
z = Song(title= 'Happiness',artist='Asake')


db.session.add(y)
db.session.add(t)
db.session.add(u)
db.session.add(q)
db.session.add(y)
db.session.add(z)
db.session.commit()


play1 = PlaylistSong(playlist_id=a.id, song_id=y.id)
play2 = PlaylistSong(playlist_id=a.id, song_id=t.id)

play3 = PlaylistSong(playlist_id=b.id, song_id=u.id)
play4 = PlaylistSong(playlist_id=b.id, song_id=q.id)

play5 = PlaylistSong(playlist_id=d.id, song_id=y.id)
play6 = PlaylistSong(playlist_id=d.id, song_id=z.id)

db.session.add(play1)
db.session.add(play2)
db.session.add(play3)
db.session.add(play4)
db.session.add(play6)
db.session.commit()


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

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

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

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    # curr_on_playlist = [s.id for s in playlist.songs]
    # form.song.choices = (db.session.query(Song.id, Song.title)
    #                      .filter(Song.id.notin_(curr_on_playlist)).all())

    curr_on_playlist = [s.id for s in playlist.songs]
    form.song.choices = [
    (song.id, song.title) for song in db.session.query(Song.id, Song.title)
    .filter(Song.id.notin_(curr_on_playlist))
    .all()]       

    if form.validate_on_submit():

        # song = Song.query.get(form.song.data)
        # playlist.songs.append(song)

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
