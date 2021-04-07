from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from models import db, User, connect_db
from flask_bcrypt import Bcrypt
from forms import AddUserForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_exercise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
bcrypt = Bcrypt()
connect_db(app)

@app.route('/')
def root():
    """Redirect to /register"""
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
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

@app.route('/login', methods=['GET', 'POST'])
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
    # need to add logic for showing Feedback from user
    if 'username' not in session: 
        flash("Please log in first to view this")
        return redirect('/login')
    user = User.query.get(username)
    print(user.username)
    if user == None:
        return redirect('/login')
    return render_template('logged_in.html',user=user)

@app.route('/logout', methods=['POST'])
def process_logout():
    session.pop('username')
    return redirect(url_for('show_login'))

@app.route('/logout', methods=['GET'])
def redirect_logout():
    """Only accept logout requests made via post"""
    return redirect(url_for('show_login'))

# routes to work on tomorrow
# need to add FeedbackForm

@app.route('/users/<username>/delete', methods=['POST'])
def delete_account(username):
    return redirect('/')

@app.route('users/<username>/feedback/add', methods=['GET', 'POST'])
def handle_feedback_form(username):
    form = FeedbackForm()
    return render_template('add_feedback.html')

@app.route('feedback/<feedback_id>/update', methods=['GET', 'POST'])
def handle_feedback_update(feedback_id):
    form = FeedbackForm()
    return redirect(url_for('show_logged_in', username=session['username']))

@app.route('feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = db.session.get(feedback_id)
    db.session.delete(feedback)
    db.session.commit()
    return redirect(url_for('show_logged_in', username=session['username']))