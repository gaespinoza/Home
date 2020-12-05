import os
import urllib
from flask import Flask, Response
import micawber
from micawber import bootstrap_basic, parse_html
from micawber.cache import Cache as OEmbedCache
from playhouse.flask_utils import FlaskDB, get_object_or_404, object_list

from flask_bcrypt import Bcrypt
from flask_login import LoginManager



APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = False
SITE_WIDTH = 800

app = Flask(__name__)
app.config.from_object(__name__)

app.config['SECRET_KEY'] = '147b88cbc5fed3de1be796e2841816a2065b1f027945faa3'

flask_db = FlaskDB(app)
database = flask_db.database

oembed_providers = bootstrap_basic(OEmbedCache())

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@app.template_filter('clean_querystring')
def clean_querystring(request_args, *keys_to_remove, **new_values):
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)
    querystring.update(new_values)
    return urllib.urlencode(querystring)


from mycode import routes