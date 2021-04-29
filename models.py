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
    posts = db.relationship('Post', backref='user')

# class Post:
# table name would be posts
# primary key will be id, which:
  # integer that autoincrements
# title will be:
  # text(50)
  # nullable to false
# content will be:
  # text, no length limit
  # nullable to false
#created_at, which:
  # type of timestamp with time zone
  # set default time to current time
# user_id as a foreign key
  #nullable to false
  #int
  # something to think about: orphan children, if we want to delete the user

class Post(db.Model):
    """Posts"""
    
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(50),
                        nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                            server_default=db.func.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)# could potentially remove this to account for orphan children situations
