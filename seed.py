from models import Playlist, PlaylistSong,Song, db
from flask_sqlalchemy import SQLAlchemy

a = Playlist(name="Jazz", description='Groove for days')
b = Playlist(name="Bluez", description='Night jolly')
c = Playlist(name="Pop", description='Mood setter')
d = Playlist(name="Afro", description='Dance the sweats off')

db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.add(d)
db.session.commit()


y = Song(title= 'we could be heros',artist='Claire',)
u = Song(title= 'danc with my father',artist='Luther')
t = Song(title= 'Best night',artist='Usher',)
q = Song(title= 'Hit em',artist='2Pac',)
y = Song(title= 'yeye',artist='Burna Boy',)
z = Song(title= 'Happiness',artist='Asake',)


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