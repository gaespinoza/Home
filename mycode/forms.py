from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mycode.models import User


# class AdminRegistrationForm(FlaskForm):
# 	username = StringField('Username', validators=[DataRequired()])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
# 	passcode = PasswordField('Passcode', validators=[DataRequired()])
# 	confirm_passcode= PasswordField('Confirm Passcode', validators=[DataRequired(), EqualTo('passcode')])
# 	submit = SubmitField('Register')

# 	def validate_username(self, username):
# 		user = AdminUser.query.filter_by(username=username.data).first()
# 		if user:
# 			raise ValidationError('That username is taken.')

# class AdminLoginForm(FlaskForm):
# 	username = StringField('Username', validators=[DataRequired()])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	passcode = IntegerField('Passcode', validators=[DataRequired()])
# 	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password= PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	userphoto = FileField('Upload Club Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is taken.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is taken.')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign In')
