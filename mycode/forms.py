from flask import request
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from mycode.models import User, Entry

#Registration form
# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     passcode = StringField('Passcode', validators=[DataRequired()])
#     confirm_passcode = StringField('Confirm Passcode', validators=[DataRequired(), EqualTo('passcode')])
#     is_admin = BooleanField('Admin')
#     submit = SubmitField('Register')
    
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user:
#             raise ValidationError('This username is taken.')
        
# class EntryForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    passcode = StringField('Passcode', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SearchForm(FlaskForm):
    q = StringField('Search blogs', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args 
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False 
        super(SearchForm, self).__init__(*args, **kwargs)