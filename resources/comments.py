from email import message
from os import stat
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
comment = Blueprint('comments', __name__)
from flask_login import current_user

# @comment.get('/')
# def test_comment():
#     return 'Comment blueprint works'

#### POST: create a new comment on a ticket
@comment.post('/<ticket_id>/new_comment')
def create_comment(ticket_id):
    try:
        payload = request.get_json()
        payload['created_by'] = current_user.id
        payload['ticket'] = ticket_id

        created_comment = models.Comment.create(**payload)
        created_comment_dict = model_to_dict(created_comment)

        return jsonify(
            data = created_comment_dict,
            message='Successfully added a comment!',
            status=201
        )     

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid Ticket ID',
            status=400
        ), 400

#### GET: all comments of a given ticket
@comment.get('/<ticket_id>/all_comments')
def get_all_comments(ticket_id):
    all_comments = models.Comment.select().where(models.Comment.ticket == ticket_id)
    all_comments_dict = [model_to_dict(comment) for comment in all_comments]

    return jsonify(
        data=all_comments_dict,
        message=f'Fetched {len(all_comments_dict)} tickets',
        status=200
    ), 200

# GET: a comment
@comment.get('/<comment_id>')
def show_comment(comment_id):
    try:
        comment_to_show = models.Comment.get_by_id(comment_id)
        comment_dict = model_to_dict(comment_to_show)

        return jsonify(
            data=comment_dict,
            message='Here\'s the ticket!',
            status=200
        ), 200
        

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid Ticket ID',
            status=400
        ), 400


#### PUT: edit a comment
@comment.put('/<comment_id>/edit_comment')
def edit_comment(comment_id):
    comment_to_edit = models.Comment.get_by_id(comment_id)
    try:
        payload = request.get_json()
        if comment_to_edit.created_by.id == current_user.id:
            query = models.Comment.update(**payload).where(models.Comment.id == comment_id)
            query.execute()

            updated_comment = models.Ticket.get_by_id(comment_id)
            updated_comment_dict = model_to_dict(updated_comment)
            return jsonify(
                data=updated_comment,
                status=200,
                message='Successfully updated the ticket'
            )
        else:
            return jsonify(
                data={},
                message='You dont have permissions to edit this comment',
                status=403
            ), 403        
        
    except models.DoesNotExist:
        return jsonify(
            data={},
            message='invalid comment ID',
            status=400
        ), 400    

#### DELETE: delete a comment
@comment.delete('/<comment_id>/delete_comment')
def delete_comment(comment_id):
    comment_to_delete = models.Comment.get_by_id(comment_id)
    try:
        if comment_to_delete.created_by.id == current_user.id:
            comment_to_delete.delete_instance()
            
            return jsonify(
                message='Comment deleted successfully',
                status=200
            ), 200
        
        else: 
            return jsonify(
                message='You don\'t have permission to delete the ticket',
                status=403
            ), 403

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='invalid comment ID',
            status=400
        )