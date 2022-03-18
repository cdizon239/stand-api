from flask import Flask, jsonify
from dotenv import load_dotenv
import os
import models

#  import controllers
from resources.spaces import space


load_dotenv()

DEBUG = True
PORT = os.getenv('PORT') or 8000
app = Flask(__name__)

#  register blueprints
app.register_blueprint(space, url_prefix='/api/v1/spaces')



@app.get('/')
def test_route():
    return f'app is workinggggg on {PORT}'

if __name__ == '__main__':
    models.initialize()
    app.run(
        port=PORT,
        debug=DEBUG
    )