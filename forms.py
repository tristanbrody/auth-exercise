from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Regexp, URL, NumberRange, Optional, Length

class AddUserForm(FlaskForm):
    """Form for adding a new user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=4,max=30,message="Must be between 4 and 30 characters")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email address", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Add feedbacK"""
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Your feedback", validators=[InputRequired()])


