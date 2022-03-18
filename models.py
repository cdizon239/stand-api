import os
from dotenv import load_dotenv

#  using peewee as the ORM
from peewee import *
from playhouse.db_url import connect
import datetime

load_dotenv()

# points to the database
DATABASE_URL= connect(os.getenv('DATABASE_URL'))

#### USER MODEL ####
class User(Model):
    googleId=CharField()
    name=CharField()
    email=CharField()
    img_url=CharField()

    class Meta:
        database=DATABASE_URL

#### SPACES MODEL ####
class Space(Model):
    owner=ForeignKeyField(User, backref='spaces')
    name=CharField(unique=True)
    privacy=CharField()
    is_active=BooleanField()
    # notes=
    created_at=DateTimeField(default=datetime.datetime.now)

    # the Meta class is a special class inside your model
    # that exists to just tell it how to run
    class Meta:
        database=DATABASE_URL

#### MEMBER MODEL ####
class Member(Model):
    user=ForeignKeyField(User, backref= 'members')
    space=ForeignKeyField(Space, backref= 'members')
    
    class Meta:
        database=DATABASE_URL


def initialize():
    DATABASE_URL.connect()
    # the safe keyword argument means don't create the table
    DATABASE_URL.create_tables([User, Space, Member], safe=True)

    print('TABLES CREATED')
    DATABASE_URL.close()
 