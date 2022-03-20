from email import message
from itertools import count
import json
from telnetlib import STATUS
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
space = Blueprint('spaces', __name__)
from flask_login import current_user

# @space.get('/')
# def space_test():
#     return 'Space blueprint works'

#### CREATE A SPACE (WITH MEMBERS) ####
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

#### INDEX: GET ALL SPACES ####
@space.get('/')
def spaces_index():
    all_spaces = models.Space.select()
    spaces_dict = [model_to_dict(space) for space in all_spaces]

    # count_members = models.Space.select(models.Space, fn.Count(models.User).alias('member_count')).join(models.SpaceMember).join(models.User).group_by(models.Space)

    return jsonify(
        data = spaces_dict,
        message = f'Fetched {len(spaces_dict)} spaces',
        status = 201
    ), 201

#### Get a space ###
@space.get('/<space_id>')
def show_space(space_id):
    try:
        space_to_show = models.Space.get_by_id(space_id)
        space_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == space_id)
        space_members_dlist = [model_to_dict(member) for member in space_members]
        print(space_members_dlist)
        space_dict = model_to_dict(space_to_show)
        space_dict['members'] = space_members_dlist
        
        return jsonify(
            data=space_dict,
            message='Successfully fetched the space',
            status= 200
        ), 200

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Space ID is invalid',
            status= 400
        ), 400

#### EDIT A SPACE ####
@space.put('/<space_id>')
def edit_space(space_id):
    try:
        space_to_update = models.Space.get_by_id(id)
        if space_to_update.owner.id ==  current_user.id:
            payload = request.get_json()
            query = models.Space.update(**payload).where(models.Space.id == space_id)
            query.execute()

            updated_space = models.Space.get_by_id(space_id)
            space_dict = model_to_dict(updated_space)

            return jsonify(
                data=space_dict,
                status=200,
                message=f"Succefully updated {space_dict['name']}"
            )
        else:
            return jsonify(
                data={},
                status=403,
                message='You do not have permission to update the space'
            ), 403
        
        
    except models.DoesNotExist:
        return jsonify(
            data={},
            status=400,
            message='Invalid Space ID'
        ), 400

#### POST: Add members to the space ####
@space.post('/<space_id>/add_member')
def add_member(space_id):
    payload = request.get_json()
    try: 
        #  get new space members from payload
        space_members_to_add = models.User.select().where(models.User.email << payload['members'])
        new_space_members_dlist = [model_to_dict(member) for member in space_members_to_add]

        for new_member in new_space_members_dlist:
            models.SpaceMember.create(
                space = space_id,
                user = new_member['id']
            )
        members = models.SpaceMember.select()
        print([model_to_dict(member) for member in members])
        
        return jsonify(
            data={},
            message='Successfully added members',
            status=200
        ), 200
        

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid Space ID',
            status=400
        ), 400



#### DELETE A SPACE ###
@space.delete('/<space_id>')
def delete_space(space_id):
    try:
        space_to_delete = models.Space.get_by_id(space_id)
        if space_to_delete.owner.id == current_user.id:
            space_to_delete.delete_instance()
            return jsonify(
                message = 'Succefully deleleted the space',
                status = 200
            )
    except models.DoesNotExist:
        return jsonify (
            data = {},
            message = 'Invalid Space ID',
            status = 400
        ), 400


####
