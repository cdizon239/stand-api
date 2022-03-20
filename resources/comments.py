from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
comment = Blueprint('comments', __name__)
from flask_login import current_user

@comment.get('/')
def test_comment():
    return 'Comment blueprint works'