from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
ticket = Blueprint('tickets', __name__)
from flask_login import current_user

# GET: index for all tickets for a space
@ticket.get('/<space_id>/all_tickets')
def ticket_index(space_id):
    all_tickets = models.Ticket.select().where(models.Ticket.space == space_id)
    all_tickets_dict = [model_to_dict(ticket) for ticket in all_tickets]
    
    return jsonify(
        data=all_tickets_dict,
        message=f'Fetched {len(all_tickets_dict)} tickets',
        status=200
    ), 200

# POST: create a ticket
@ticket.post('/<space_id>/add_ticket')
def create_ticket(space_id):
    payload = request.get_json()
    payload['created_by'] = current_user.id
    payload['space'] = space_id

    space_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == space_id)
    space_members_id_dict = [model_to_dict(member)['user']['id'] for member in space_members]

    if current_user.id in space_members_id_dict:
        created_ticket = models.Ticket.create(**payload)
        created_ticket_dict = model_to_dict(created_ticket)

        return jsonify(
            data = created_ticket_dict,
            message = 'Successfully created a ticket',
            status = 201
        ), 201
    else:
        return jsonify(
            data={},
            message='You don\'t have permissions to create a ticket',
            status=403
        ), 403
    
# GET: one ticket
@ticket.get('/<ticket_id>')
def show_ticket(ticket_id):
    try:
        ticket_to_show = models.Ticket.get_by_id(ticket_id)
        ticket_dict = model_to_dict(ticket_to_show)

        return jsonify(
            data=ticket_dict,
            message='Here\'s the ticket!',
            status=200
        ), 200
        

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid Ticket ID',
            status=400
        ), 400

#  tickets should be able to be updated by anyone in the space
@ticket.patch('/<ticket_id>/edit')
def edit_ticket(ticket_id):
    try:
        print('yay')
        
        ticket_to_edit = models.Ticket.get_by_id(ticket_id)
        space_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == ticket_to_edit.space)
        space_members_id_dict = [model_to_dict(member)['user']['id'] for member in space_members]
        print(space_members_id_dict)
        print(current_user.id)

        if current_user.id in space_members_id_dict:
            print('yay')
            payload = request.get_json()
            query = models.Ticket.update(**payload).where(models.Ticket.id == ticket_id)
            query.execute()

            updated_ticket = models.Ticket.get_by_id(ticket_id)
            updated_ticket_dict = model_to_dict(updated_ticket)
            return jsonify(
                data=updated_ticket_dict,
                status=200,
                message='Successfully updated the ticket'
            )
        
        else:
            # send back an error if the wrong user is logged in
            return jsonify(
                data={},
                status=403,
                message='You do not have permission to edit that ticket'
            ), 403

    except models.DoesNotExist:
        return jsonify(
            data={},
            message='Invalid ticket ID',
            status=400,
        ), 400

### delete ticket
@ticket.delete('/<ticket_id>/delete')
def delete_ticket(ticket_id):
    ticket_to_delete = models.Ticket.get_by_id(ticket_id)
    try:
        space_members = models.SpaceMember.select(models.SpaceMember.user).where(models.SpaceMember.space == ticket_to_delete.space)
        space_members_id_dict = [model_to_dict(member)['user']['id'] for member in space_members]
        print(space_members_id_dict)

        if current_user.id in space_members_id_dict:
            ticket_to_delete.delete_instance()
            
            return jsonify(
                message='Ticket deleted successfully',
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
            message='invalid Ticket ID',
            status=400
        ), 400
        
