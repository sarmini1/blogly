"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "shhhhhhhhh"

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """renders homepage html"""
    users = User.query.all()
    return render_template('homepage.html', users = users)