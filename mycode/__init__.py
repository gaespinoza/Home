import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
import urllib
from elasticsearch import Elasticsearch
from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)


if os.environ.get('ENV'):
    ENV = 'prod'
else:
    ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:localDev@localhost/blog'
    app.config['SECRET_KEY'] = '147b88cbc5fed3de1be796e2841816a2065b1f027945faa3'
    app.config['ELASTICSEARCH_URL'] = 'http://localhost:9200'
elif ENV == 'prod':
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['ELASTICSEARCH_URL'] = os.environ.get('ELASTICSEARCH_URL')
    app.config['LOG_TO_STDOUT'] = os.environ.get('LOG_TO_STDOUT')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['POSTS_PER_PAGE'] = 25

# if app.config['LOG_TO_STDOUT']:
#     stream_handler = logging.StreamHandler()
#     stream_handler.setLevel(logging.INFO)
#     app.logger.addHandler(stream_handler)
# else:
#     if not os.path.exists('logs'):
#         os.mkdir('logs')
#     file_handler = RotatingFileHandler('logs/home.log', maxBytes=10240, backupCount=10)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s '
#         '[in %(pathname)s:%(lineno)d]'
#     ))
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
# app.logger.setLevel(logging.INFO)
# app.logger.info('Home starting')

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None



db = SQLAlchemy(app)



bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from mycode.models import User, Entry, MyModelView, MyAdminIndexView

admin = Admin(app, index_view=MyAdminIndexView(), name='home', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Entry, db.session))



# @app.template_filter('clean_querystring')
# def clean_querystring(request_args, *keys_to_remove, **new_values):
#     querystring = dict((key, value) for key, value in request_args.items())
#     for key in keys_to_remove:
#         querystring.pop(key, None)
#     querystring.update(new_values)
#     return urllib.urlencode(querystring)


from mycode import routes