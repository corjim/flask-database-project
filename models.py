"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""
    with app.app_context():
        db.app = app
        db.init_app(app)

# db.drop_all()
# db.create_all()


class Playlist(db.Model):
    """Playlist table"""
    
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Establish many-to-many relationship with Song through PlaylistSong
    songs = db.relationship("Song", secondary="playlists_songs", backref="playlists")

    def __repr__(self):
        """show info about post"""
        p = self 
        return f'<Playlists id = {p.id}, Name: {p.name}, Description = {p.description}'

class Song(db.Model):
    """Table for Songs"""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    artist = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """show info about post"""
        p = self 
        return f'<Title = {p.title}, artist = {p.artist}'
    


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = 'playlists_songs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

    def __repr__(self):
        """show info about post"""
        p = self 
        return f'<Playlist id = {p.playlist_id}, song id = {p.song_id}'
    

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
