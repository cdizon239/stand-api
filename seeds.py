from peewee import *
import models

# Users seed data

users = [
    {'googleId':'1fefcsdffe', 'name':'Thai Huynh' ,'email':'thai@gmail.com','img_url':'ncsfnoewim'},
    {'googleId':'1fefsdknsde', 'name':'Charmille Dizon' ,'email':'char@gmail.com','img_url':'ncefejnewim'},
    {'googleId':'1fefc3458e', 'name':'Irene Dizon' ,'email':'irene@gmail.com','img_url':'ncssbdfusnwim'}
]

# Spaces seed data
spaces = [
    {'owner': 1, 'name': 'Hogwarts v2', 'privacy':'private'},
    {'owner': 2, 'name': 'Narnia v2', 'privacy':'private'},
    {'owner': 3, 'name': 'Wonderland v2', 'privacy':'public'}
]

# SpaceMembers seed data
space_members = [
    {'space': 1, 'user': 1},
    {'space': 1, 'user': 2},
    {'space': 2, 'user': 2},
    {'space': 2, 'user': 3},
    {'space': 3, 'user': 1},
    {'space': 3, 'user': 2},
    {'space': 3, 'user': 3}
]

# Tickets seed data
tickets = [
    {'space':1,'status': 'To do','title': 'Practice new spell', 'created_by': 1},
    {'space':1,'status': 'In Progress','title': 'Drink butter beer!', 'created_by': 2},
    {'space':1,'status': 'Blocked','title': 'Spy on snape', 'created_by': 1},
    {'space':1,'status': 'Done','title': 'Play quidditch!', 'created_by': 2},
]

# Comments seed data

comments = [
    {'ticket': 2, 'detail': 'I won\'t be able to make it to drinks', 'created_by': 1 },
    {'ticket': 2, 'detail': 'Okay we can do it next time', 'created_by': 2}
]

models.User.insert_many(users).execute()
models.Space.insert_many(spaces).execute()
models.SpaceMember.insert_many(space_members).execute()
models.Ticket.insert_many(tickets).execute()
models.Comment.insert_many(comments).execute()