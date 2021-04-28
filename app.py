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

@app.route('/users/new')
def show_add_user_form():
    """Routes user to form to add new user"""
    return render_template('add_user_form.html')

@app.route('/users/new', methods = ['POST'])
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']
    img_url = img_url if img_url else None

    user = User(first_name = first_name, last_name = last_name, image_url = img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>')
def display_user_info(user_id):
    user = User.query.get(user_id)
    return render_template('display_user_info.html', user = user)
