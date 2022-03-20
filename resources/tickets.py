from email import message
from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
from peewee import *
import models
ticket = Blueprint('tickets', __name__)
from flask_login import current_user

# GET: index for all tickets
@ticket.get('/')
def ticket_index():
    all_tickets = models.Ticket.select()
    all_tickets_dict = [model_to_dict(ticket) for ticket in all_tickets]
    
    return jsonify(
        data=all_tickets_dict,
        message=f'Fetched {len(all_tickets_dict)} tickets',
        status=200
    ), 200

# POST: create a ticket
@ticket.post('/<space_id>/add_ticket')
def create_ticket():
    payload = request.get_json()
    payload['owner'] = current_user.id
    
    created_ticket = models.Ticket.create(**payload)
    created_ticket_dict = model_to_dict(created_ticket)

    return jsonify(
        data = created_ticket_dict,
        message = 'Successfully created a ticket',
        status = 201
    ), 201
    
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
