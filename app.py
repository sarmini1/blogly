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
def redirects_to_users():
    """redirects to /users"""
    return redirect('/users')

@app.route('/users')
def displays_users():
    """renders user list html"""
    users = User.query.all()
    return render_template('user_list.html', users = users)

@app.route('/users/new')
def show_add_user_form():
    """Routes user to form to add new user"""
    return render_template('add_user_form.html')

@app.route('/users/new', methods = ['POST'])
def add_user():
    """adds new user to database and redirects to user list"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']
    img_url = img_url if img_url else None

    user = User(first_name=first_name, 
                last_name=last_name, 
                image_url=img_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user_info(user_id):
    """displays user profile"""
    user = User.query.get_or_404(user_id)
    return render_template('display_user_info.html', user=user)

@app.route('/users/<int:user_id>/edit') 
def display_edit_user_form(user_id):
    """displays edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user_info.html', user=user)   

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    """changes existing users info in database and redirects to user list"""
    user = User.query.get_or_404(user_id)

    first_name = request.form['first_name']
    user.first_name = first_name if first_name else user.first_name

    last_name = request.form['last_name']
    user.last_name = last_name if last_name else user.last_name

    img_url = request.form['img_url']
    user.image_url = img_url if img_url else user.image_url

    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST']) 
def delete_user(user_id):
    """delete user from database and redirects to user list"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')   