"""Seed file to make sample data for users db."""

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
whiskey = User(first_name='Whiskey', last_name="Dog")
bowser = User(first_name='Bowser', last_name="Pug")
spike = User(first_name='Spike', last_name="Porcupine")

#Add posts 
user_1_post_1 = Post(title = "my first post", content = "a;skldjfa;skldfjsa", user_id = 1)
user_1_post_2 = Post(title = "my second post", content = "sdlfkldfksj", user_id = 1)
user_2_post_1 = Post(title = "cool stuff", content = "this is user 2's post", user_id = 2)
user_3_post_1 = Post(title = "something", content = "a;skldjfa;skldfjsa", user_id = 3)
user_3_post_2 = Post(title = "user three enjoys these things", content = "some things here", user_id = 3)
user_3_post_3 = Post(title = "third post", content = "beep", user_id = 3)

# Add new objects to session, so they'll persist
db.session.add(whiskey)
db.session.add(bowser)
db.session.add(spike)

# Commit the users!
db.session.commit()

# Add new posts to session
db.session.add(user_1_post_1)
db.session.add(user_1_post_2)
db.session.add(user_2_post_1)
db.session.add(user_3_post_1)
db.session.add(user_3_post_2)
db.session.add(user_3_post_3)

# Commit--otherwise, this never gets saved!
db.session.commit()