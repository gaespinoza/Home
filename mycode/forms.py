from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from mycode.models import User

#Registration form
# class RegistrationForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     passcode = StringField('Passcode', validators=[DataRequired()])
#     confirm_passcode = StringField('Confirm Passcode', validators=[DataRequired(), EqualTo('passcode')])
#     submit = SubmitField('Register')
    
#     def validate_username(self, username):
#         print(type(User))
#         names = User.select()
#         for name in names:
#             if name == username.data:
#                 raise ValidationError('This username is taken.')
        

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    passcode = StringField('Username', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')