from mycode import db, app, login_manager, ModelView, AdminIndexView
from mycode.search import add_to_index, remove_from_index, query_index
from flask import render_template, url_for, redirect, request, flash, abort
from flask_login import UserMixin, current_user

import datetime as datetime
import re

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total
        
    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add' : list(session.new),
            'update' : list(session.dirty),
            'delete' : list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None 

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    passcode = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
	
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"

    @property 
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True


class Entry(SearchableMixin, db.Model):

    __searchable__ = ['content']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    slug = db.Column(db.String(64), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    media = db.Column(db.String(64), nullable=False)
    published = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub('[^\w]+','-',self.title.lower())

    @classmethod
    def public(cls):
        
        return Entry.query.filter_by(published=True).all()

    @classmethod
    def drafts(cls):
        return Entry.query.filter_by(published=False).all()

class MyModelView(ModelView):
    

    def is_accessible(self):
        
        return (current_user.is_authenticated and current_user.is_admin == True)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))
        
