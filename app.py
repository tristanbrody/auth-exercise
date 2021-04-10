from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from models import db, User, Feedback, connect_db
from flask_bcrypt import Bcrypt
from forms import AddUserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
bcrypt = Bcrypt()
connect_db(app)
LOGIN_ROOT = '/login'

#TODO clean up view functions by moving most of the logic to some sort of controller

@app.route('/')
def root():
    """Redirect to /register"""
    if 'username' in session:
        return redirect(url_for('show_logged_in', username=session['username']))
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('show_logged_in', username=session['username']))
    form = AddUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect(url_for('show_logged_in', username=session['username']))
    return render_template('sign_up.html', form=form)

@app.route(LOGIN_ROOT, methods=['GET', 'POST'])
def show_login():
    if 'username' in session:
        return redirect(url_for('show_logged_in', username=session['username']))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            flash("Incorrect username or password")
    return(render_template('login.html', form=form))

@app.route('/users/<username>')
def show_logged_in(username):
    if 'username' not in session: 
        flash("Please log in first to view this")
        return redirect(LOGIN_ROOT)
    user = User.query.get(session['username'])
    if user == None:
        return redirect(LOGIN_ROOT)
    if user.is_admin: 
        feedback = Feedback.query.all()
    else: 
        feedback = Feedback.query.filter_by(username=session['username']).all()
    form = FeedbackForm()
    return render_template('logged_in.html',user=user, form=form, feedback=feedback)

@app.route('/logout', methods=['POST'])
def process_logout():
    session.pop('username')
    return redirect(url_for('show_login'))

@app.route('/logout', methods=['GET'])
def redirect_logout():
    """Only accept logout requests made via post"""
    flash("Please log out from your account")
    return redirect(url_for('show_login'))

@app.route('/users/<username>/delete', methods=['POST'])
def delete_account(username):
    if 'username' not in session: 
        flash("Please log in")
        return redirect(LOGIN_ROOT)
    user = User.query.get(session['username'])
    if user == None:
        return redirect(LOGIN_ROOT)
    if username != session['username'] and not user.is_admin: 
        return redirect('/')
    User.query.delete(username)
    db.session.commit()
    flash("Your account has been deleted")
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['POST'])
def handle_feedback_form(username):
    if 'username' not in session:
        flash("Please log in to post feedback")
        return redirect(url_for('show_login'))
    if username != session['username']:
        flash("You can't post feedback for somebody else's account!")
        return redirect(url_for('show_logged_in'))
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
    new_feedback = Feedback(title=title,content=content,username=username)
    db.session.add(new_feedback)
    db.session.commit()
    flash("Your feedback has been added")
    return redirect(url_for('show_logged_in', username=session['username']))

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def handle_feedback_update(feedback_id):
    if 'username' not in session:
        flash("Please log in to post feedback")
        return redirect(url_for('show_login'))

    feedback = Feedback.query.get(feedback_id)
    if feedback == None:
        return redirect(url_for('show_logged_in', username=session['username']))
    if feedback.username != session['username']:
        flash("You can't update feedback for somebody else's account!")
        return redirect(url_for('show_logged_in', username=session['username']))
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = feedback.content.data
        flash("Your feedback was updated")
        return redirect(url_for('show_logged_in', username=session['username']))
    return render_template('edit_feedback.html', form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    if 'username' not in session:
        flash("Please log in to delete feedback")
        return redirect(url_for('show_login'))
    feedback = Feedback.query.get(feedback_id)
    if feedback == None:
        return redirect(url_for('show_logged_in', username=session['username']))
    if feedback.username != session['username']:
        flash("You can't delete feedback for somebody else's account!")
        return redirect(url_for('show_logged_in', username=session['username']))
    db.session.delete(feedback)
    db.session.commit()
    flash("Your post has been deleted")
    return redirect(url_for('show_logged_in', username=session['username']))

#helper functions

def check_if_logged_in():
    if 'username' in session:
        redirect(url_for('show_logged_in', username=session['username']))