from typing import Text
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, IntegerField, SelectField, DecimalField, TextAreaField, RadioField
#from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, ValidationError, length, optional

class loginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class createUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class activateForm(FlaskForm):
    play_key = StringField('Play Key', validators=[DataRequired()], render_kw={"placeholder": "Play Key", "class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email", "class": "form-control"})
    name = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username", "class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control"})
    password2 = PasswordField('Repeat Password', validators=[DataRequired()], render_kw={"placeholder": "Repeat Password", "class": "form-control"})
    submit = SubmitField('Create Account', render_kw={"class": "btn btn-primary"})

class renameCharacterForm(FlaskForm):
    requested_name = StringField('Requested Name', validators=[DataRequired()], render_kw={"placeholder": "Requested Name", "class": "form-control"})
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})