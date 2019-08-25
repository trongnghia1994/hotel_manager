# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields, EmbeddedMongoModel


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
    def find_room_inventory(id):
        return RoomInventory.objects.get({'_id': ObjectId(id)})
