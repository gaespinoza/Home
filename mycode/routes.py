from mycode import app, bcrypt
from flask import render_template, url_for, redirect, request, flash
from mycode.forms import AdminLoginForm
import secrets
import os
import string
import datetime

@app.route("/", methods =["GET"])
@app.route("/index", methods =["GET"])
def index():
	return render_template('/index.html')

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

@app.route("/adminlogin", methods = ["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = AdminLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and bcrypt.check_password_hash(user.passcode, form.passcode.data):
			next_page = request.args.get('next')
			login_user(user)
			flash("Login successful...", "success")
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash("Login failed", "danger")
	return render_template('/adminlogin.html', form=form)