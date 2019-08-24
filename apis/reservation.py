from datetime import datetime

from flask_restplus import Namespace, Resource, fields, reqparse

from core.helpers.reservation_helper import confirm_reservation, create_reservation
from core.models import Reservation
from decorators import login_required
from common import authorizations

api = Namespace('reservation', description='Reservation related operations', authorizations=authorizations)

reservation_fields = api.model('Reservation', {
    '_id': fields.String(readonly=True, example="5d60fee168a3ff141856cba2"),
    'status': fields.String(readonly=True, example="pending"),
    'room_inventory_id': fields.String(required=True, example="5d60fee168a3ff141856cba2"),
    'check_in': fields.String(required=True, example="2019-08-24T09:00:00.000Z"),
    'check_out': fields.String(required=True, example="2019-08-25T09:00:00.000Z"),
    'adults': fields.Integer(required=True, example=2),
    'children': fields.Integer(required=True, example=1),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String(required=True),
    'message': fields.String(required=True),
})

re_parser = reqparse.RequestParser()
re_parser.add_argument('hotel_id', required=True, help='Hotel id cannot be blank')


@api.route('/')
class ReservationsResource(Resource):
    @api.expect(re_parser)
    @api.marshal_list_with(reservation_fields)
    def get(self):
        '''Get reservations'''
        args = re_parser.parse_args()
        reservations = Reservation.find_by_hotel(args['hotel_id'])
        return list(reservations), 200

    @api.doc(security='authToken')
    @api.expect(reservation_fields, validate=True)
    @api.marshal_with(reservation_fields, code=201, mask='_id')
    def post(self):
        '''Create reservation'''
        reservation = create_reservation(api.payload)
        return reservation, 201


conf_parser = reqparse.RequestParser()
conf_parser.add_argument('conf_number', required=True, help='Conf number cannot be blank')


@api.doc(security='authToken')
@api.route('/<string:reservation_id>/confirmation')
class ReservationResource(Resource):
    @login_required("reservation.confirm")
    @api.expect(conf_parser)
    @api.marshal_with(reservation_fields, mask='_id,status')
    def put(self, token_data, reservation_id):
        '''Confirm reservation'''
        args = conf_parser.parse_args()
        data = confirm_reservation(reservation_id, args["conf_number"])
        return data, 200
