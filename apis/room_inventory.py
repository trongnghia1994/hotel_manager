from datetime import datetime

from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse

from core.helpers.room_inventory_helper import search
from core.models import RoomInventory
from decorators import login_required
from common import authorizations

api = Namespace('roomInventory', description='RoomInventory related operations', authorizations=authorizations)

daily_rates_fields = api.model('Daily Rates', {
    'date': fields.DateTime(required=True, example="2019-08-25T00:00:00.000Z"),
    'quantity': fields.Integer(required=True, example=10),
    'remain': fields.Integer(required=True, example=10),
    'rate': fields.Float(required=True, rate=1.0),
})

room_inventory_fields = api.model('Room Inventory', {
    '_id': fields.String(readonly=True),
    'description': fields.String(readonly=True),
    'name': fields.String(required=True),
    'accommodation_id': fields.String(required=True, example="5d5ffb9968a3ff1ee8237d99"),
    'sell_start_date': fields.String(required=True, example="2019-08-24T00:00:00.000Z"),
    'sell_end_date': fields.String(required=True, example="2019-08-26T00:00:00.000Z"),
    'daily_rates': fields.List(fields.Nested(daily_rates_fields)),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

ri_parser = reqparse.RequestParser()
ri_parser.add_argument('hotel_id', location='args', help='Hotel id cannot be blank')


@api.route('/')
class RoomInventoriesResource(Resource):
    @login_required(permission='inventory.view')
    @api.expect(ri_parser)
    @api.marshal_list_with(room_inventory_fields)
    def get(self, token_data):
        '''Get room inventories'''
        args = ri_parser.parse_args()
        room_inventories = RoomInventory.find_by_hotel(args['hotel_id'])
        return list(room_inventories), 200

    @api.doc(security='authToken')
    @api.expect(room_inventory_fields, validate=True)
    @api.marshal_with(room_inventory_fields, code=201, mask='_id')
    @login_required(permission='inventory.add')
    def post(self, token_data):
        '''Create room inventory'''
        print api.payload
        room_inventory = RoomInventory.from_document(api.payload)
        room_inventory.created_at = datetime.utcnow()
        return room_inventory.save(), 201


search_parser = reqparse.RequestParser()
search_parser.add_argument('hotel_id', required=True, help='Hotel id cannot be blank')
search_parser.add_argument('checkIn', required=True, help='Checkin cannot be blank')
search_parser.add_argument('checkOut', required=True, help='Checkout cannot be blank')
search_parser.add_argument('adults', type=int, required=True, help='Adults cannot be blank')


@api.route('/availableItems')
class AvailableRoomInventoriesResource(Resource):
    @api.expect(search_parser)
    @api.marshal_list_with(room_inventory_fields)
    def get(self):
        '''Search available room inventories'''
        args = search_parser.parse_args()
        data = search(args)
        return data, 200
