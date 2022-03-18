from flask import Blueprint
import models


space = Blueprint('spaces', __name__)

@space.get('/')
def space_test():
    return 'Space blueprint works'

