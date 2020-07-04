import os
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'abc'

from mycode import routes