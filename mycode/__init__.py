import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin

import os.path as op


app = Flask(__name__)

app.config['SECRET_KEY'] = '147b88cbc5fed3de1be796e2841816a2065b1f027945faa3'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'



bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mycode.models import User, Comment, Post, MyModelView#, MyAdminIndexView

admin = Admin(app, name='home', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))

path = op.join(op.dirname(__file__), 'static/documents')
admin.add_view(FileAdmin(path, '/static/documents', name='Documents'))


from mycode import routes
