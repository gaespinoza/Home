from mycode import db, login_manager, app, ModelView
from flask import render_template, url_for, redirect, request, flash
from flask_login import UserMixin, current_user
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# @login_manager.user_loader
# def load_adminuser(adminuser_id):
# 	return AdminUser.query.get(int(adminuser_id))

# class AdminUser(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(64), nullable=False)
# 	password = db.Column(db.String(60), nullable=False)
# 	passcode = db.Column(db.String(60), nullable=False)
# 	posts = db.relationship('Post', backref='author', lazy=True)

# 	def __repr__(self):
# 		return f"User('{self.username}', '{self.id}')"

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	email = db.Column(db.String(64), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(64), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	comments = db.relationship('Comment', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.id}')"

	@property 
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property 
	def is_anonymous(self):
		return False

	

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(250), nullable=True)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	comments = db.relationship('Comment', backref='post', lazy=True)

	def __repr__(self):
		return f"User('{self.title}', '{self.description}', '{self.date_posted}')"

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(500), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

	def __repr__(self):
		return f"Comment('{self.id}', '{self.date_posted}', '{self.user_id}')"

class MyModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))


# class MyAdminIndexView(object):
# 	def is_accessible(self):
# 		return current_user.is_authenticated

	# def inaccessible_callback(self, name, **kwargs):
	# 	return redirect(url_for('login'))
	
		