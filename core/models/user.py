# -*- coding: utf-8 -*-
from datetime import datetime

from bson import ObjectId
from pymodm import MongoModel, fields


class User(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.CharField()
    password = fields.CharField()
    role = fields.ObjectIdField()
    superuser = fields.BooleanField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    @staticmethod
    def find_user(email, password):
        return User.objects.get({'email': email, 'password': password})


class Role(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    name = fields.CharField()
    permissions = fields.ListField(fields.ObjectIdField(), default=[])
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())

    def find_permissions(self):
        '''Find permissions belonging to this role'''
        permissions = Permission.objects.raw({'_id': {'$in': self.permissions}})
        return [p.name for p in list(permissions) if permissions]


class Permission(MongoModel):
    _id = fields.ObjectIdField(primary_key=True, default=ObjectId())
    name = fields.CharField()
    created_at = fields.DateTimeField()
    updated_at = fields.DateTimeField(default=datetime.utcnow())
