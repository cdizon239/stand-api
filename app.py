from urllib import response
from flask import Flask, jsonify, g
from dotenv import load_dotenv
from flask_cors import CORS
import os
import models

#  import controllers
from resources.spaces import space
from resources.users import user
from resources.tickets import ticket
from resources.comments import comment

#  auth dependencies
from flask_login import LoginManager

#  twilio dependencies
import uuid  # for generating random user id values
import twilio.jwt.access_token
import twilio.jwt.access_token.grants
import twilio.rest

app = Flask(__name__)
load_dotenv()
CORS(app, supports_credentials=True)

SESSION_SECRET = os.getenv('SESSION_SECRET')
DEBUG = True
PORT = os.getenv('PORT') or 8000

#### LOGIN MANAGER ####
app.secret_key = SESSION_SECRET
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    # the user_loader expects to get an id for a user
    # and it expects us to return a user if it exists
    # and None if it does not exist
    try:
        return models.User.get_by_id(user_id)
    except models.DoesNotExist:
        return None

#  REGISTER BLUEPRINTS
app.register_blueprint(space, url_prefix='/api/v1/spaces')
app.register_blueprint(user, url_prefix='/api/v1/users')
app.register_blueprint(ticket, url_prefix='/api/v1/tickets')
app.register_blueprint(comment, url_prefix='/api/v1/comments')

#  CORS CONFIG
CORS(space, supports_credentials=True)
CORS(user, supports_credentials=True)
CORS(ticket, supports_credentials=True)
CORS(comment, supports_credentials=True)


@app.before_request
def before_request():
    '''Connect to the database before each request'''
    g.db = models.DATABASE_URL
    g.db.connect()

@app.after_request
def after_request(response):
    '''Close db connection after each request'''
    g.db.close()
    return response

@app.get('/')
def test_route():
    return f'app is workinggggg on {PORT}'

if __name__ == '__main__':
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )

#  Twilio sources https://www.twilio.com/docs/video/tutorials/get-started-with-twilio-video-python-flask-server
# https://www.lohani.dev/blog/integrate-twilio-video-into-a-react-application