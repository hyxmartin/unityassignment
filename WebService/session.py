import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# setx DBUSER "postgres"
# setx DBPASS "Temp@Win2000"
# setx DBHOST "localhost"
# setx DBNAME "postgres"

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)


# Create our database model
class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.String(50))
    country = db.Column(db.String(50))
    event = db.Column(db.String(50),)
    session_id = db.Column(db.String(255))
    ts = db.Column(db.Time(timezone=False))

    def __init__(self, player_id, country, event, session_id, ts):
        self.player_id = player_id
        self.country = country
        self.event = event
        self.session_id = session_id
        self.ts = ts
