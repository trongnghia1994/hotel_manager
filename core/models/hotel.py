# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields


class Hotel(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    name = fields.CharField()
    description = fields.CharField()
    timezone = fields.CharField()
    address = fields.CharField()
    website = fields.CharField()
    logo_url = fields.CharField(default='')
    cover_url = fields.CharField(default='')
    loyalty_club = fields.CharField(default='')
    loyalty_url = fields.CharField(default='')
    currency = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    @staticmethod
    def find_hotel(id):
        return Hotel.objects.get({'_id': ObjectId(id)})
