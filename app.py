"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    user = User(first_name=first_name, 
                last_name=last_name, 
                image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def display_user_info(user_id):
    """displays user profile"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template('display_user_info.html',
                            user=user, posts=posts)

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

    image_url = request.form['image_url']
    user.image_url = image_url if image_url else user.image_url

    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ['POST']) 
def delete_user(user_id):
    """delete user from database and redirects to user list"""
    user = User.query.get_or_404(user_id)
    Post.query.filter(Post.user_id == user_id).delete()
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')   

@app.route('/users/<int:user_id>/posts/new')
def display_add_new_post_form(user_id):
    """renders add new post for user html"""
    user = User.query.get_or_404(user_id)
    return render_template('add_post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """add new post to database and redirects to user info page"""
    title = request.form['title']
    content = request.form['content']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def display_post_page(post_id):
    """renders post detail page html"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail_page.html', post=post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_user_post(post_id):
    """deletes post from database and redirects to user info page"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id):
    """displays edit post form"""
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post_form.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit_post_form(post_id):
    """handles edit post form submit and redirects back to post page"""
    post = Post.query.get_or_404(post_id)

    title = request.form['title']
    post.title = title if title else post.title

    content = request.form['content']
    post.content = content if content else post.content

    db.session.commit()
    
    return redirect(f'/posts/{post_id}')