import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_security import Security, SQLAlchemyUserDatastore

import os.path as op


app = Flask(__name__)

app.config['SECRET_KEY'] = '147b88cbc5fed3de1be796e2841816a2065b1f027945faa3'



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
# app.config['SECURITY_PASSWORD_SALT'] = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'



bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# roles_users = db.Table(
#     'roles_users',
#     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
# )

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mycode.models import User, Comment, Post, MyModelView, MyFileView

admin = Admin(app, name='home', template_mode='bootstrap3')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Post, db.session))
admin.add_view(MyModelView(Comment, db.session))

# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

path = op.join(op.dirname(__file__), 'static/documents')
admin.add_view(MyFileView(path, '/static/documents', name='Documents'))


from mycode import routes
