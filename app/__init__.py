from flask import Flask 

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


#import all the routes from the routes file into the current folder 
from . import routes 