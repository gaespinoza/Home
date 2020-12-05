from mycode import app, database, bcrypt
from mycode.forms import LoginForm #, RegistrationForm
from mycode.models import Entry, FTSEntry, User
from flask import render_template, url_for, redirect, request, flash, session, abort, Markup, Response
from flask_login import current_user, login_user, logout_user, login_required
from playhouse.sqlite_ext import *
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list
import secrets
import os
import string
import datetime
import functools


@app.route("/", methods =["GET"])
@app.route("/index", methods =["GET"])
def index():
	return render_template('index.html')

#Code used to create registration
# @app.route("/register", methods=['GET','POST'])
# def register():
# 	if current_user.is_authenticated:
# 		return redirect(url_for('index'))
# 	form = RegistrationForm()
# 	if form.validate_on_submit():
# 		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
# 		hashed_passcode = bcrypt.generate_password_hash(form.passcode.data).decode('utf-8')
# 		user = User(username=form.username.data, password=hashed_password, passcode=hashed_passcode)
# 		user.save()
# 		flash('Your account has been created', 'success')
# 		return redirect(url_for('login'))
# 	return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()	
	if request.method == 'POST' and request.form.get('password'):
		user = User.get(User.username==form.username.data)
		if user and bcrypt.check_password_hash(user.password, form.password.data) and bcrypt.check_password_hash(user.passcode, form.passcode.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Login Failed. Check credentials.', 'danger')
	return render_template('login.html', form=form)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/experience", methods = ["GET"])
def experience():
	return render_template('/experience.html')

@app.route("/blogs", methods = ["GET"])
def blogs():
	search_query = request.args.get('q')
	if search_query:
		query = Entry.search(search_query)
	else:
		query = Entry.public().order_by(Entry.timestamp.desc())
	return object_list('blogs.html', query, search=search_query, check_bounds=False)

def _create_or_edit(entry, template):
	if request.method == 'POST':
		entry.title = request.form.get('title') or ''
		entry.content = request.form.get('content') or ''
		entry.published = request.form.get('published') or False
		entry.media = request.form.get('media') or ''
		delete = request.form.get('delete') or False		
		if (delete == 'y'):
			entry.delete_instance()
			return redirect(url_for('blogs'))
		elif not (entry.title and entry.content):
			flash('Title and Content are required.', 'danger')
		else:
			entry.save()
			flash('Entry Saved Successfully', 'success')
			if entry.published:
				return redirect(url_for('detail', slug=entry.slug))
			else:
				return redirect(url_for('edit', slug=entry.slug))
	return render_template(template, entry=entry)

@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	return _create_or_edit(Entry(title='', content=''), 'create.html')	

@app.route('/drafts/')
@login_required
def drafts():
	query = Entry.drafts().order_by(Entry.timestamp.desc())
	return object_list('blogs.html', query, check_bounds=False)

@app.route('/<slug>/')
def detail(slug):
	if session.get('logged_in'):
		query = Entry.select()
	else:
		query = Entry.public()
	entry = get_object_or_404(query, Entry.slug == slug)
	return render_template('detail.html', entry=entry)

@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
	entry = get_object_or_404(Entry, Entry.slug == slug)
	return _create_or_edit(entry, 'edit.html')

@app.route("/resources", methods = ["GET"])
def resources():
	return render_template('/resources.html')

@app.route("/games", methods = ["GET"])
def games():
	return render_template('/games.html')

@app.route("/music", methods = ["GET"])
def music():
	return render_template('/music.html')

