# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields


class Reservation(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    check_in = fields.DateTimeField()
    check_out = fields.DateTimeField()
    adults = fields.IntegerField()
    children = fields.IntegerField()
    room_inventory_id = fields.ObjectIdField()
    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.CharField()
    phone = fields.CharField()
    message = fields.CharField()
    conf_number = fields.CharField(default='undefined')
    status = fields.CharField(choices=('pending', 'confirmed', 'cancelled'), default='pending')
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    @staticmethod
    def find_reservation(id):
        return Reservation.objects.get({"_id": ObjectId(id)})
