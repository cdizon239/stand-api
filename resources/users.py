from cmath import log
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, logout_user

load_dotenv()

from google.oauth2 import id_token
from google.auth.transport import requests

import models
user = Blueprint('users', __name__)
GCLIENT_ID = os.getenv('GCLIENT_ID')
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

def verify(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        google_user = id_token.verify_oauth2_token(token, requests.Request(), GCLIENT_ID)
        
        user_info = {
            "name": google_user['name'],
            "email": google_user['email'],
            "img_url": google_user['picture'],
            "googleId": google_user['sub'],
        }
        return user_info
        
    except ValueError:
        #invalid token
        pass

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
    #  verify google token
    google_user = verify(payload['id_token'])
    print(google_user)
    
    try:
        user_to_login = models.User.get(models.User.email == google_user['email'])
        user_dict = model_to_dict(user_to_login)

        login_user(user_to_login)
        
        return jsonify(
            data=user_dict,
            message='User logged in',
            status=200
        ), 200

    except models.DoesNotExist:
        created_user = models.User.create(**google_user)
        login_user(created_user)
        user_dict = model_to_dict(created_user)

        return jsonify(
            data = user_dict,
            message = 'User logged in',
            status = 200
        ), 200

@user.get('/me')
def get_user():
    try:
        current_user = models.User.get_by_id(current_user.id)
        current_user_dict = model_to_dict(current_user)

        return jsonify(
            data=current_user_dict,
            message='My info',
            status=200
        ), 200

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Could not fetch info for that user',
            status=400
        ), 400

@user.post('/register')
def register():
    payload = request.get_json()
    try:
        google_user = verify(payload['token'])
        user_to_login = models.User.get(models.User.email == google_user['email'])
        models.User.get(models.User.email == google_user['email'])

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