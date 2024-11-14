# models.py

import mongoengine as me
from bson import ObjectId
from datetime import datetime

class Product(me.Document):
    name = me.StringField(required=True)
    description = me.StringField()
    price = me.DecimalField(required=True)
    category_id = me.ObjectIdField(required=True)  # This will reference a category from the Categories collection
    variants = me.ListField(me.DictField())
    images = me.ListField(me.StringField())
    created_at = me.DateTimeField()
    updated_at = me.DateTimeField()

    meta = {
        'collection': 'products'  # Ensure this is the correct collection name in MongoDB
    }


class Category(me.Document):
    # Define the fields and their types as per the JSON schema
    name = me.StringField(required=True, max_length=255)
    description = me.StringField(default=None)
    created_at = me.DateTimeField(default=datetime.now)
    updated_at = me.DateTimeField(default=datetime.now)
    
    # Ensure that the category name is unique if necessary
    meta = {
        'collection': 'categories',  # MongoDB collection name
        'indexes': [
            {'fields': ['name'], 'unique': True}  # Unique index on 'name'
        ]
    }