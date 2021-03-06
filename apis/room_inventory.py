from datetime import datetime

from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse

from common import authorizations
from core.helpers.room_inventory_helper import find_room_inventories_by_hotel, search
from core.models import RoomInventory
from decorators import login_required

api = Namespace('roomInventory', description='RoomInventory related operations', authorizations=authorizations)

daily_rates_fields = api.model('Daily Rates', {
    'date': fields.DateTime(required=True, example="2019-08-25"),
    'quantity': fields.Integer(required=True, example=10),
    'remain': fields.Integer(required=True, example=10),
    'rate': fields.Float(required=True, rate=20.0),
})

room_inventory_fields = api.model('Room Inventory', {
    '_id': fields.String(readonly=True),
    'description': fields.String(readonly=True),
    'name': fields.String(required=True),
    'accommodation_id': fields.String(required=True, example="5d5ffb9968a3ff1ee8237d99"),
    'sell_start_date': fields.String(required=True, example="2019-08-24"),
    'sell_end_date': fields.String(required=True, example="2019-08-26"),
    'daily_rates': fields.List(fields.Nested(daily_rates_fields)),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})

ri_parser = reqparse.RequestParser()
ri_parser.add_argument('hotel_id', location='args', help='Hotel id cannot be blank. Eg: 5d5ff40668a3ff060c2df835')


@api.route('/')
class RoomInventoriesResource(Resource):
    @api.doc(security='authToken', responses={200: 'Success', 401: 'Unauthorized', 403: 'Forbidden'})
    @login_required(permission='inventory.view')
    @api.expect(ri_parser)
    @api.marshal_list_with(room_inventory_fields)
    def get(self, token_data):
        '''Get room inventories'''
        args = ri_parser.parse_args()
        room_inventories = find_room_inventories_by_hotel(args['hotel_id'])
        return list(room_inventories), 200

    @api.doc(security='authToken', responses={401: 'Unauthorized', 403: 'Forbidden'})
    @api.expect(room_inventory_fields, validate=True)
    @api.marshal_with(room_inventory_fields, code=201, description='Created', mask='_id')
    @login_required(permission='inventory.add')
    def post(self, token_data):
        '''Create room inventory'''
        room_inventory = RoomInventory.from_document(api.payload)
        room_inventory.created_at = datetime.utcnow()
        return room_inventory.save(), 201


search_parser = reqparse.RequestParser()
search_parser.add_argument('hotel_id', required=True, help='Hotel id cannot be blank. Eg: 5d5ff40668a3ff060c2df835')
search_parser.add_argument('checkIn', required=True, help='Checkin cannot be blank. Eg: 2019-08-25')
search_parser.add_argument('checkOut', required=True, help='Checkout cannot be blank. Eg: 2019-08-26')
search_parser.add_argument('adults', type=int, required=True, help='Adults cannot be blank. Eg: 3')


@api.route('/availableItems')
@api.doc(responses={200: 'Success'})
class AvailableRoomInventoriesResource(Resource):
    @api.expect(search_parser)
    @api.marshal_list_with(room_inventory_fields)
    def get(self):
        '''Search available room inventories'''
        args = search_parser.parse_args()
        data = search(args)
        return data, 200
