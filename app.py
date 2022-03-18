from flask import Flask
from dotenv import load_dotenv
import os


load_dotenv()

DEBUG = True
PORT = 8000

app = Flask(__name__)

@app.get('/')
def test_route():
    return 'app is workinggggg'

if __name__ == '__main__':
    app.run(
        port=PORT,
        debug=DEBUG
    )