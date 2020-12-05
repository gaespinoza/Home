from mycode import flask_db, app, database, oembed_providers, login_manager
from flask import render_template, url_for, redirect, request, flash, abort, Markup
from flask_login import UserMixin, current_user
from micawber import bootstrap_basic, parse_html
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from peewee import *
from playhouse.sqlite_ext import *
import datetime as datetime
import re

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

class User(flask_db.Model, UserMixin):
    username = CharField(unique=True)
    password = CharField(unique=True)
    passcode = CharField(unique=True)
	
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"

    @property 
    def is_authenticated(self):
        return True
        
    @property
    def is_active(self):
        return True


class Entry(flask_db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    media = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub('[^\w]+','-',self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)

        self.update_search_index()
        return ret 

    def update_search_index(self):
        search_content = '\n'.join((self.title, self.content))
        try:
            fts_entry = FTSEntry.get(FTSEntry.docid == self.id)
        except FTSEntry.DoesNotExist:
            FTSEntry.create(docid=self.id, content=search_content)
        else:
            fts_entry.content = search_content
            fts_entry.save()

    @classmethod
    def public(cls):
        
        return Entry.select().where(Entry.published == True)

    @classmethod
    def search(cls, query):
        words = [word.strip() for word in query.split() if word.strip()]
        if not words:
            return Entry.select().where(Entry.id == 0)
        else:
            search = ' '.join(words)

        return(Entry
        .select(Entry, FTSEntry.rank().alias('score'))
        .join(FTSEntry, on=(Entry.id == FTSEntry.docid))
        .where(
            (Entry.published == True) & 
            (FTSEntry.match(search)))
        .order_by(SQL('score')))

    @classmethod
    def drafts(cls):
        return Entry.select().where(Entry.published == False)

    @property
    def html_content(self):
        hilite = CodeHiliteExtension(linenums=False,css_class='highlight')
        extras = ExtraExtension()
        if self.media:
            markdown_content = markdown(self.content, extensions=[hilite, extras])
        else:
            markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)
        

class FTSEntry(FTSModel):
    content = SearchField()
 
    class Meta:
        database = database