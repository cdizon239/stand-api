import os
from dotenv import load_dotenv

#  using peewee as the ORM
from peewee import *
from playhouse.db_url import connect
import datetime

# auth dependencies
from flask_login import UserMixin

load_dotenv()

# points to the database
DATABASE_URL= connect(os.getenv('DATABASE_URL'))

#### USER MODEL ####
class User(UserMixin, Model):
    googleId=CharField()
    name=CharField()
    email=CharField()
    img_url=CharField()
    created_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=DATABASE_URL

#### SPACES MODEL ####
class Space(Model):
    owner=ForeignKeyField(User, backref='spaces_owned')
    name=CharField(unique=True)
    privacy=CharField()
    is_active=BooleanField(default=True)
    created_at=DateTimeField(default=datetime.datetime.now)

    # the Meta class is a special class inside your model
    # that exists to just tell it how to run
    class Meta:
        database=DATABASE_URL

#### SPACE MEMBER MODEL ####
class SpaceMember(Model):
    user=ForeignKeyField(User, backref= 'space_members')
    space=ForeignKeyField(Space, backref= 'space_members')
    
    class Meta:
        database=DATABASE_URL

#### TICKET MODEL ####     
class Ticket(Model):
    space=ForeignKeyField(Space, backref='space_tickets')
    status=CharField()
    title=CharField()
    description=TextField(null=True)
    assignee=ForeignKeyField(User, backref='ticket_assignee', null=True)
    likes=IntegerField(default=0)
    created_by=ForeignKeyField(User, backref='ticket_reporter')
    created_at=DateTimeField(default=datetime.datetime.now)
    updated_at=DateTimeField(default=datetime.datetime.now)
    is_archived=BooleanField(default=False)

    class Meta:
        database=DATABASE_URL

#### COMMENT MODEL ####     
class Comment(Model):
    ticket=ForeignKeyField(Ticket, backref='ticket_comments')
    detail=TextField()
    likes=IntegerField(default=0)
    created_by=ForeignKeyField(User, backref='ticket_author')
    created_at=DateTimeField()
    updated_at=DateTimeField(default=datetime.datetime.now)

    class Meta:
        database=DATABASE_URL        


def initialize():
    DATABASE_URL.connect()
    # the safe keyword argument means don't create the table
    DATABASE_URL.create_tables([User, Space, Ticket, Comment, SpaceMember], safe=True)

    print('TABLES CREATED')
    DATABASE_URL.close()
 