"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = "https://pbs.twimg.com/profile_images/1064544692707172354/LuZuUIkr_400x400.jpg"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

# class User:
# tablename would be "users"
# each entry should have the primary key of id, which:
  # is an integer type, auto-increments 
# each entry should have separate values for first and last name, which:
  # could be text type
  # set nullable to false
# each entry should have a value for image url, which:
  # text type, don't want to limit the length here
  # set nullable to false
  # provide a default value in case one is not provided

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.Text,
                            nullable = False)
    last_name = db.Column(db.Text,
                            nullable = False)
    image_url = db.Column(db.Text,
                            nullable = False,
                            default = DEFAULT_IMG)
