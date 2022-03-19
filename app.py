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

app.secret_key = SESSION_SECRET
#  set up login manager 
login_manager = LoginManager()
login_manager.init_app(app)

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