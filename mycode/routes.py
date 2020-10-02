from mycode import app, db, bcrypt
from mycode.models import User, Post, Comment
from mycode.forms import RegistrationForm, LoginForm

from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required

import secrets
import os
import string
import datetime

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
	return redirect(url_for('home'))

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