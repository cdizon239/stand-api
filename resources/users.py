from email import message
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user

import models
user = Blueprint('users', __name__)

# @user.get('/')
# def test_users():
#     return 'User blueprint worksss'

@user.get('/')
def get_users():
    users = models.User.select()
    dict_users = [model_to_dict(user) for user in users]
    return jsonify(
        data=dict_users,
        status=201,
        message=f'returned {len(dict_users)} users'
    )

@user.post('/login')
def login():
    payload = request.get_json()
    try:
        user_to_login = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user_to_login)

        login_user(user_to_login)
        
        return jsonify(
            data=user_dict,
            message='User logged in',
            status=200
        ), 200

    except models.DoesNotExist:
        return jsonify(
            data = {},
            status = 401,
            message = 'User not signed up on the app yet!'
        ), 401

@user.post('/register')
def register():
    payload = request.get_json()

    try:
        models.User.get(models.User.email == payload['email'])

        return jsonify(
            data = {},
            status=401,
            message='A user with that email already exists'
        ), 401

    except models.DoesNotExist:
        created_user = models.User.create(**payload)
        login_user(created_user)
        user_dict = model_to_dict(created_user)

        return jsonify(
            data = user_dict,
            message = 'User logged in',
            status = 200
        ), 200

@user.get('/logout')
def logout():
    logout_user()

    return jsonify(
        status = 200,
        message = 'Succesfully logged out'
    ), 200