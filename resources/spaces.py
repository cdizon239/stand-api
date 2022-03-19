from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict
import models
space = Blueprint('spaces', __name__)



# @space.get('/')
# def space_test():
#     return 'Space blueprint works'

@space.post('/')
def create_space():
    payload = request.get_json()
    #  grab all the members that need to be added to a space

    create_space = models.Space.create(
        name=payload['name'],
        privacy=payload['privacy'],
    )
    created_space = model_to_dict(create_space)
    return jsonify(
        data=created_space,
        message='Space created!',
        status=201
    ), 201


    




    


