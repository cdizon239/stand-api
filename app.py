from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import models

#  import controllers
from resources.spaces import space
from resources.users import user

#  auth dependencies
from flask_login import LoginManager

app = Flask(__name__)
load_dotenv()

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

#  register blueprints
app.register_blueprint(space, url_prefix='/api/v1/spaces')
app.register_blueprint(user, url_prefix='/api/v1/users')



@app.get('/')
def test_route():
    return f'app is workinggggg on {PORT}'

if __name__ == '__main__':
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )