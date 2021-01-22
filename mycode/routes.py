from mycode import app, bcrypt, db
from mycode.forms import LoginForm, RegistrationForm, SearchForm
from mycode.models import Entry, User
from flask import render_template, url_for, redirect, request, flash, session, abort, Markup, Response, g, current_app
from flask_login import current_user, login_user, logout_user, login_required



import secrets
import os
import string
import datetime
import functools

@app.before_request
def before_request():
	g.search_form = SearchForm()
	


@app.route("/", methods =["GET"])
@app.route("/index", methods =["GET"])
def index():
	return render_template('index.html')

#Code used to create registration
@app.route("/register", methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		hashed_passcode = bcrypt.generate_password_hash(form.passcode.data).decode('utf-8')
		user = User(username=form.username.data, password=hashed_password, passcode=hashed_passcode, is_admin=form.is_admin.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login/', methods=["GET", "POST"])
def login():
	
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()	
	if form.validate_on_submit:
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data) and bcrypt.check_password_hash(user.passcode, form.passcode.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index'))
		else:
			flash('Login Failed. Check credentials.', 'danger')
	return render_template('login.html', form=form)

@app.route('/logout/', methods=["GET", "POST"])
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route("/experience", methods = ["GET"])
def experience():
	return render_template('/experience.html')

@app.route("/blogs", methods = ["GET", "POST"])
def blogs():
	
	page = request.args.get('page', 1, type=int)
	posts = Entry.query.filter_by(published=True).paginate(
		page, current_app.config['POSTS_PER_PAGE'], False
	)
	next_url = url_for('blogs', page=posts.next_num) if posts.has_next else None

	prev_url = url_for('blogs', page=posts.prev_num) if posts.has_prev else None

	

	return render_template('blogs.html', title='Explore',
	posts = posts.items, next_url=next_url, prev_url=prev_url)
	

@app.route("/search")
def search():
	
	if not g.search_form.validate():
		
		return redirect(url_for('blogs'))
	
	page = request.args.get('page', 1, type=int)
	
	posts, total = Entry.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
	
	next_url = url_for('search', q=g.search_form.q.data, page = page + 1) if total > page * current_app.config['POSTS_PER_PAGE'] else None
	prev_url = url_for('search', q=g.search_form.q.data, page = page - 1) if page > 1 else None
	return render_template('blogs.html', title='Search', posts=posts, next_url=next_url, prev_url=prev_url )

def _create_or_edit(entry, template, md):
	if request.method == 'POST':
		
		entry.title = request.form.get('title') or ''
		entry.content = request.form.get('editordata') or ''
		pub = request.form.get('published')
		entry.media = request.form.get('media') or ''
		delete = request.form.get('delete') or False
		
		if (pub == 'True'):
			entry.published = True		
		if (delete == 'True'):
			
			db.session.delete(entry)
			
			db.session.commit()
			return redirect(url_for('blogs'))
		elif not (entry.title and entry.content):
			flash('Title and Content are required.', 'danger')
		else:
			if md == 'c':
				db.session.add(entry)
			
			entry.save()
			db.session.commit()
			flash('Entry Saved Successfully', 'success')
			if entry.published:
				return redirect(url_for('detail', slug=entry.slug))
			else:
				return redirect(url_for('edit', slug=entry.slug))
	return render_template(template, entry=entry)

@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	return _create_or_edit(Entry(title='', content=''), 'create.html', 'c')	

@app.route('/drafts/')
@login_required
def drafts():
	posts = Entry.query.filter_by(published=False).all()
	
	
	return render_template('blogs.html', posts=posts, check_bounds=False)

@app.route('/<slug>/')
def detail(slug):
	if session.get('logged_in'):
		query = Entry.query.all()
	else:
		query = Entry.public()
	entry = Entry.query.filter_by(slug=slug).first()
	if entry:
		
		return render_template('detail.html', entry=entry)



@app.route('/<slug>/edit/', methods=['GET', 'POST'])
@login_required
def edit(slug):
	
	entry = Entry.query.filter_by(slug=slug).first()
	
	return _create_or_edit(entry, 'edit.html', 'e')

@app.route("/resources", methods = ["GET"])
def resources():
	return render_template('/resources.html')

@app.route("/games", methods = ["GET"])
def games():
	return render_template('/games.html')

@app.route("/music", methods = ["GET"])
def music():
	return render_template('/music.html')

