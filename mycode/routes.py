from mycode import app, db, bcrypt
from mycode.models import User, Post, Comment
from mycode.forms import RegistrationForm, LoginForm

from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required

import secrets
import os
import string
import datetime

# @app.before_first_request
# def before_first_request():

#     # Create any database tables that don't exist yet.
#     db.create_all()

#     # Create the Roles "admin" and "end-user" -- unless they already exist
#     user_datastore.find_or_create_role(name='admin', description='Administrator')
#     user_datastore.find_or_create_role(name='end-user', description='End user')

#     # Create two Users for testing purposes -- unless they already exists.
#     # In each case, use Flask-Security utility function to encrypt the password.
#     encrypted_password = utils.encrypt_password('password')
#     if not user_datastore.get_user('someone@example.com'):
#         user_datastore.create_user(email='someone@example.com', password=encrypted_password)
#     if not user_datastore.get_user('admin@example.com'):
#         user_datastore.create_user(email='admin@example.com', password=encrypted_password)

#     # Commit any database changes; the User and Roles must exist before we can add a Role to the User
#     db.session.commit()

#     # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
#     # Users already have these Roles.) Again, commit any database changes.
#     user_datastore.add_role_to_user('someone@example.com', 'end-user')
#     user_datastore.add_role_to_user('admin@example.com', 'admin')
#     db.session.commit()

@app.route("/")
@app.route("/index")
def index():
	return render_template('/index.html')

@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

# @app.route("/adminregister", methods=['GET','POST'])
# def adminregister():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('index'))
# 	form = AdminRegistrationForm()
# 	if form.validate_on_submit():
# 		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
# 		hashed_passcode = bcrypt.generate_password_hash(form.passcode.data).decode('utf-8')
# 		adminuser = AdminUser(username=form.username.data, password=hashed_password, passcode=hashed_passcode)
# 		db.session.add(adminuser)
# 		db.session.commit()
# 		flash('Your account has been created', 'success')
# 		return redirect(url_for('login'))
# 	return render_template('adminregister.html', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Login Failed. Check credentials.', 'danger')
	return render_template('login.html', form=form)

# @app.route("/adminlogin", methods = ["GET", "POST"])
# def adminlogin():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('index'))
# 	form = AdminLoginForm()
# 	if form.validate_on_submit():
# 		user = User.query.filter_by(username=form.username.data).first()
# 		if user and bcrypt.check_password_hash(user.password, form.password.data) and bcrypt.check_password_hash(user.passcode, form.passcode.data):
# 			login_user(user)
# 			next_page = request.args.get('next')
# 			flash("Login successful...", "success")
# 			return redirect(next_page) if next_page else redirect(url_for('index'))
# 		else:
# 			flash("Login failed", "danger")
# 	return render_template('/adminlogin.html', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
	return render_template('account.html')


@app.route("/experience", methods = ["GET"])
def experience():
	return render_template('/experience.html')

@app.route("/blog", methods = ["GET"])
def blog():
	return render_template('/blog.html')

@app.route("/resources", methods = ["GET"])
def resources():
	return render_template('/resources.html')

@app.route("/games", methods = ["GET"])
def games():
	return render_template('/games.html')

@app.route("/music", methods = ["GET"])
def music():
	return render_template('/music.html')