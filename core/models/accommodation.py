# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields


class Accommodation(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    hotel_id = fields.ObjectIdField()
    name = fields.CharField()
    description = fields.CharField()
    max_guests = fields.IntegerField()
    image_url = fields.CharField(default='')
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())
