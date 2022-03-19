from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
space = Blueprint('spaces', __name__)
from flask_login import current_user

# @space.get('/')
# def space_test():
#     return 'Space blueprint works'

@space.post('/')
def create_space():
    payload = request.get_json()
    payload['owner'] = current_user.id

    #  grab all the members that need to be added to a space
    space_members = models.User.select().where(models.User.email << payload['members'])

    #  create a space
    create_space = models.Space.create(
        owner=payload['owner'],
        name=payload['name'],
        privacy=payload['privacy'],
    )
    created_space = model_to_dict(create_space)
    space_members_dict = [model_to_dict(space_member) for space_member in space_members]
    
    # populate spacemember table for each member in space  
    for user in space_members_dict:
        models.SpaceMember.create(
            user=user['id'],
            space=created_space['id']
        )
    
    members = models.SpaceMember.select()
    print([model_to_dict(member) for member in members])

    return jsonify(
        data=created_space,
        message='Space created!',
        status=201
    ), 201

    



