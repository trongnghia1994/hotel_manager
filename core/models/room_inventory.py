# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields, EmbeddedMongoModel

from accommodation import Accommodation


class DailyRate(EmbeddedMongoModel):
    date = fields.DateTimeField()
    quantity = fields.IntegerField()
    remain = fields.IntegerField()
    rate = fields.FloatField()


class RoomInventory(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    accommodation_id = fields.ObjectIdField()
    name = fields.CharField()
    description = fields.CharField(default='')
    daily_rates = fields.EmbeddedDocumentListField(DailyRate, default=[])
    sell_start_date = fields.DateTimeField()
    sell_end_date = fields.DateTimeField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    @staticmethod
    def find_by_hotel(hotel_id):
        accommodations = Accommodation.objects.raw({'hotel_id': ObjectId(hotel_id)})
        acc_ids = [a._id for a in list(accommodations) if accommodations]
        room_inventories = RoomInventory.objects.raw({'accommodation_id': {'$in': acc_ids}})
        return room_inventories

    @staticmethod
    def find_by_id(id):
        return RoomInventory.objects.get({'_id': ObjectId(id)})
