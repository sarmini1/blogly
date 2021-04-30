"""Models for Blogly."""

import datetime
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

    def __repr__(self):
      return f'<User {self.first_name} {self.last_name}>' 

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
    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable=False)
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
      return f'<Post {self.title} {self.id}>'            


# class Tag:
#__tablename__: tags
# id: primary key, int
# name: text, unique, not null
# tag.posts

class Tag(db.Model):
  """ Tags. """
  __tablename__ = "tags"

  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)

  name = db.Column(db.Text,
                    nullable=False,
                    unique=True)               

  def __repr__(self):
    return f'<Tag {self.name} {self.id}>' 

#class PostTag:
#__tablename__: posts_tags
#post_id: foreign key, primary key
#tag_id: foreign key, primary key

class PostTag(db.Model):
  """Posts + Tags"""
  __tablename__ = "posts_tags"

  post_id = db.Column(db.Integer,
                      db.ForeignKey("posts.id"),
                      primary_key=True)

  tag_id = db.Column(db.Integer,
                      db.ForeignKey("tags.id"),
                      primary_key=True)                      

  def __repr__(self):
    return f'<PostTag {self.post_id} {self.tag_id}>'
