#  resource: https://www.twilio.com/docs/video/tutorials/get-started-with-twilio-video-python-flask-server
from cmath import log
import os
#  twilio dependencies
import uuid  # for generating random user id values
import twilio.jwt.access_token
import twilio.jwt.access_token.grants
import twilio.rest
from flask import Blueprint, request

video = Blueprint('video', __name__)

from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
api_key = os.getenv('TWILIO_API_KEY_SID')
api_secret = os.getenv('TWILIO_API_KEY_SECRET')
twilio_client = twilio.rest.Client(api_key, api_secret, account_sid)

def find_or_create_room(room_name):
    try:
        # try to fetch an in-progress room with this name
        twilio_client.video.rooms(room_name).fetch()
    except twilio.base.exceptions.TwilioRestException:
        # the room did not exist, so create it
        twilio_client.video.rooms.create(unique_name=room_name)

def get_access_token(room_name):
    # create the access token
    access_token = twilio.jwt.access_token.AccessToken(
        account_sid, api_key, api_secret, identity=uuid.uuid4().int
    )
    # create the video grant
    video_grant = twilio.jwt.access_token.grants.VideoGrant(room=room_name)
    # Add the video grant to the access token
    access_token.add_grant(video_grant)
    return access_token

@video.post("/join_room")
def join_room():
    payload = request.get_json()
    # extract the room_name from the JSON body of the POST request
    room_name = payload['room_name']
    # find an existing room with this room_name, or create one
    find_or_create_room(room_name)
    # retrieve an access token for this room
    access_token = get_access_token(room_name)
    # return the decoded access token in the response
    # NOTE: if you are using version 6 of the Python Twilio Helper Library,
    # you should call `access_token.to_jwt().decode()`
    print({
        "token": access_token.to_jwt(),
        "username": payload['identity']
    })
    
    return {
        "token": access_token.to_jwt(),
        "username": payload['identity']
        }