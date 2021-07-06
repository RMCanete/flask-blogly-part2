"""Blogly application."""

from flask import Flask, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2118@localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'asdfghjkl'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():

    return redirect('users')

@app.route('/users')
def show_users():
  
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users=users)

@app.route('/users/new', methods=['GET'])
def new_user_form():
    
    return render_template('users/create_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route(f"/users/<int:user_id>")
def show_user_info(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('users/user_details.html', user=user)

@app.route(f"/users/<int:user_id>/edit")
def show_edit_user_page(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)

@app.route(f"/users/<int:user_id>/edit", methods=['POST'])
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name'],
    user.last_name = request.form['last_name'],
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')    

@app.route(f"/users/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# /////////////////////////////////////////////////////////////////////////

@app.route("/users/<int:user_id>/posts/new", methods=['GET'])
def show_new_post_form(user_id):
    
    user = User.query.get_or_404(user_id)
    return render_template('/posts/new_post.html', user=user)


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def handle_new_post_form(user_id):
    
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title= request.form['title'],
        content = request.form['content'], user=user)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')    

@app.route("/posts/<int:post_id>", methods=['GET'])
def show_post(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show_post.html', post=post)

@app.route(f"/posts/<int:post_id>/edit", methods=['GET'])
def show_edit_post_form(post_id):
    
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/edit_post.html', post=post)

@app.route(f"/posts/<int:post_id>/edit", methods=['POST'])
def handle_edit_post_form(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.title= request.form['title'],
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')    

@app.route(f"/posts/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')
