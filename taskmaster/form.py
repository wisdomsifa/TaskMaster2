from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from taskmaster.models import User, Task
import email_validator

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2 , max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is taken, choose a different username.')
        
    def email_validator(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('The email is taken, choose a different email.')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2 , max=20)])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    title = StringField('Task Title:', validators=[DataRequired(), Length(min=2 , max=20)])
    description = TextAreaField('Description:', validators=[DataRequired()])
    creator = StringField('Creator:', validators=[DataRequired(), Length(min=2 , max=50)])
    submit = SubmitField('Add')
