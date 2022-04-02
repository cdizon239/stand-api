from cmath import log
from email import message
from reprlib import recursive_repr
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
space = Blueprint('spaces', __name__)
from flask_login import current_user

#### CREATE A SPACE (WITH MEMBERS) ####
@space.post('/')
def create_space():
    payload = request.get_json()
    print(current_user)
    payload['owner'] = current_user.id
    current_user_email = model_to_dict(models.User.get_by_id(current_user.id))['email']
    
    if 'members' in payload and len(payload['members']) > 0:
        payload['members'].append(current_user_email)
    else:
        payload['members'] = [current_user_email]
    print(payload['members'])

    try:
        #  create a space
        create_space = models.Space.create(
            **payload
        )
        created_space = model_to_dict(create_space)

        #  grab all the members that need to be added to a space
        space_members = models.User.select().where(models.User.email << payload['members'])
        space_members_dict = [model_to_dict(space_member) for space_member in space_members]
        print(space_members_dict)
        
        # populate spacemember table for each member in space  
        for user in space_members_dict:
            print(user)
            models.SpaceMember.create(
                user=user['id'],
                space=created_space['id']
            )

        return jsonify(
            data=created_space,
            message='Space created!',
            status=201
        ), 201
    
    except models.DoesNotExist:
        return jsonify(
            data={},
            message='model does not exist, no Space',
            status=400
        ), 400


#### INDEX: GET ALL SPACES ####
@space.get('/')
def spaces_index():
    try:
        print(current_user.is_authenticated)
        all_spaces = models.Space.select()
        spaces_dict = [model_to_dict(space) for space in all_spaces]

        # count_members = models.Space.select(models.Space, fn.Count(models.User).alias('member_count')).join(models.SpaceMember).join(models.User).group_by(models.Space)
        return jsonify(
            data = spaces_dict,
            message = f'Fetched {len(spaces_dict)} spaces',
            status = 201
        ), 201
    
    except models.DoesNotExist:
        return jsonify(
            data={},
            message='model does not exist',
            status=400
        ), 400

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
        space_to_update = models.Space.get_by_id(space_id)
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

#### PATCH: Archive a space ####
@space.patch('/archive/<space_id>')
def archive_space(space_id):
    try:
        space_to_archive = models.Space.get_by_id(space_id)
        if space_to_archive.owner.id == current_user.id:
            payload = request.get_json()
            space_to_archive.is_active = False
            space_to_archive.save()
            
            updated_channel = models.Space.get_by_id(space_id)
            updated_channel_dict = model_to_dict(updated_channel)

            return jsonify(
                data=updated_channel_dict,
                status=200,
                message='Space successfully archived'
            ), 200

    except models.DoesNotExist:
        return jsonify(
            data={},
            status=400,
            message='Invalid Space ID'
        ), 400



@space.get('/<space_id>/space_members')
def get_all_space_members(space_id):
    current_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == space_id)

    try:
        current_members_dict = [model_to_dict(member)['user']for member in current_members]
        
        return jsonify(
            data=current_members_dict,
            message=f'fetched {len(current_members_dict)} members in the space',
            status=200
        ), 200  
        
    except models.DoesNotExist:
        return jsonify(
            data={},
            status=400,
            message='Invalid Space ID'
        ), 400





#### POST: Add members to the space ####
@space.post('/<space_id>/add_members')
def add_member(space_id):
    payload = request.get_json()
    try: 
        #  get space memebrs to add from payload
        space_members_to_add = models.User.select().where(models.User.email << payload['members'])
        space_members_to_add_dlist = [model_to_dict(member) for member in space_members_to_add]

        #  get a list of ids of current members
        current_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == space_id)
        current_members_id_dict = [model_to_dict(member)['user']['id'] for member in current_members]
        
        #  add membere to space if they are not already in the current member list
        for new_member in space_members_to_add_dlist:            
            if new_member['id'] not in current_members_id_dict:
                models.SpaceMember.create(
                    space = space_id,
                    user = new_member['id']
                )
        # return current space members
        members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == space_id)
        space_members = [model_to_dict(member) for member in members]
        
        return jsonify(
            data=space_members,
            message=f'Successfully added members, space has now {len(space_members)} members',
            status=200
        ), 200     

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid Space ID',
            status=400
        ), 400

#  come back to see if this should be change to payload members
#### DELETE: Member from a space ####
@space.delete('/<space_id>/remove_member/<user_id>')
def remove_member(space_id, user_id):
    try:
        #  remove member from SpaceMember
        member_to_remove = models.SpaceMember.delete().where((models.SpaceMember.space == space_id) & (models.SpaceMember.user == user_id))
        member_to_remove.execute()
        
        return jsonify(
            message='Successfully removed member from the space',
            status=200
        ), 200

    except models.DoesNotExist:
        return jsonify(
            message='Space member succesfully deleted',
            status=400
        ), 400


#### DELETE A SPACE ###
@space.delete('/<space_id>')
def delete_space(space_id):
    space_to_delete = models.Space.get_by_id(space_id)
    try:
        # space_to_delete = models.Space.get_by_id(space_id)
        if space_to_delete.owner.id == current_user.id:
            space_to_delete.delete_instance()
            delete_space_members = models.SpaceMember.delete().where(models.SpaceMember.space == space_id)
            delete_space_members.execute()
            return jsonify(
                message = 'Succefully deleleted the space',
                status = 200
            )
        else:
            return jsonify (
            data = {},
            message = 'Not authorized to delete',
            status = 403
        ), 403
    except models.DoesNotExist:
        return jsonify (
            data = {},
            message = 'Invalid Space ID',
            status = 400
        ), 400