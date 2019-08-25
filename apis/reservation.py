from flask_restplus import Namespace, Resource, fields, reqparse

from common import authorizations
from core.helpers.reservation_helper import confirm_reservation, create_reservation, find_reservations_by_hotel
from decorators import login_required

api = Namespace('reservation', description='Reservation related operations', authorizations=authorizations)

reservation_fields = api.model('Reservation', {
    '_id': fields.String(readonly=True, example="5d60fee168a3ff141856cba2"),
    'status': fields.String(readonly=True, example="pending"),
    'room_inventory_id': fields.String(required=True, example="5d60fee168a3ff141856cba2"),
    'check_in': fields.String(required=True, example="2019-08-24T09:00:00.000Z"),
    'check_out': fields.String(required=True, example="2019-08-25T09:00:00.000Z"),
    'adults': fields.Integer(required=True, example=2),
    'children': fields.Integer(required=True, example=1),
    'first_name': fields.String(required=True, example="Nghia"),
    'last_name': fields.String(required=True, example="Nguyen"),
    'email': fields.String(required=True, example="nghia@gmail.com"),
    'phone': fields.String(required=True, example="84xxx"),
    'message': fields.String(required=True, example="Sample message"),
})

re_parser = reqparse.RequestParser()
re_parser.add_argument('hotel_id', required=True, help='Hotel id cannot be blank. Eg: 5d5ff40668a3ff060c2df835')


@api.route('/')
class ReservationsResource(Resource):
    @api.doc(responses={200: 'Success'})
    @api.expect(re_parser)
    @api.marshal_list_with(reservation_fields)
    def get(self):
        '''Get reservations'''
        args = re_parser.parse_args()
        reservations = find_reservations_by_hotel(args['hotel_id'])
        return list(reservations), 200

    @api.expect(reservation_fields, validate=True)
    @api.marshal_with(reservation_fields, code=201, description='Created', mask='_id')
    def post(self):
        '''Create reservation'''
        reservation = create_reservation(api.payload)
        return reservation, 201


conf_parser = reqparse.RequestParser()
conf_parser.add_argument('conf_number', required=True, help='1: confirmed, 0: cancelled', choices=('1', '0'))


@api.doc(security='authToken', responses={200: 'Success', 401: 'Unauthorized'})
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
