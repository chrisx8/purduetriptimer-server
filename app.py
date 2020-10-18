import os
import secrets
from flask import Flask
from flask_restful import Api


# generate random session key
def create_session_key(length):
    key = ""
    characters = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        key += secrets.choice(characters)
    print("Created a new session key")
    return key

# create the webapp and api instances
app = Flask(__name__, instance_relative_config=True)
app_api = Api(app)

# make a secret key (length 64)
app.config.from_mapping(SECRET_KEY=create_session_key(64))

# get config url from environment var or config.py
if os.environ.get('DATABASE_URL'):
    app.config.from_envvar('DATABASE_URL')
else:
    app.config.from_pyfile('config.py')