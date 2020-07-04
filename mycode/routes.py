from mycode import app
from flask import render_template, url_for, redirect, request, flash
import secrets
import os
import string
import datetime

@app.route("/")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route("/experience", methods = ["GET"])
def experience():
	return render_template('experience.html')

@app.route("/blog", methods = ["GET"])
def blog():
	return render_template('blog.html')

@app.route("/resources", methods = ["GET"])
def resources():
	return render_template('resources.html')

@app.route("/games", methods = ["GET"])
def games():
	return render_template('games.html')

@app.route("/music", methods = ["GET"])
def music():
	return render_template('music.html')