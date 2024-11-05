"""Forms for playlist app."""

from wtforms import SelectField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired,Optional


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField('Play list Name', validators=[InputRequired(message='Add name of playlist')])
    description = StringField("Play list Description", validators=[Optional()])



class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Song Title', validators=[InputRequired(message='Add a song title')])

    artist = StringField("Song Artist", validators=[InputRequired(message="Please an artise")])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
