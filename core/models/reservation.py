# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields

from accommodation import Accommodation
from room_inventory import RoomInventory


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
    conf_number = fields.CharField(default='pending')
    status = fields.CharField(choices=('pending', 'confirmed', 'cancelled'), default='pending')
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    @staticmethod
    def get_by_id(id):
        return Reservation.objects.get({"_id": ObjectId(id)})

    @staticmethod
    def find_by_hotel(hotel_id):
        accommodations = Accommodation.objects.raw({'hotel_id': ObjectId(hotel_id)})
        acc_ids = [a._id for a in list(accommodations) if accommodations]
        room_inventories = RoomInventory.objects.raw({'accommodation_id': {'$in': acc_ids}})
        ri_ids = [ri._id for ri in list(room_inventories) if room_inventories]
        reservations = Reservation.objects.raw({'accommodation_id': {'$in': ri_ids}})
        return reservations
