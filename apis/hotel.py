from datetime import datetime

from flask_restplus import Namespace, Resource, fields

from core.models.hotel import Hotel
from decorators import login_required

api = Namespace('hotel', description='Hotel related operations')

hotel_fields = api.model('Hotel', {
    '_id': fields.String(readonly=True),
    'name': fields.String(required=True, example="Intercontinental SG"),
    'description': fields.String(required=True),
    'timezone': fields.String(required=True),
    'currency': fields.String(required=True),
    'address': fields.String(required=True, example="Saigon"),
    'website': fields.String(required=True),
    'logo_url': fields.String(readonly=True),
    'cover_url': fields.String(readonly=True),
    'loyalty_club': fields.String(readonly=True),
    'loyalty_url': fields.String(readonly=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})


@api.route('/')
@api.doc(security='authToken', responses={401: 'Unauthorized'})
class HotelResource(Resource):
    @login_required("hotel.add")
    @api.expect(hotel_fields, validate=True)
    @api.marshal_with(hotel_fields, code=201, description='Created', mask='_id')
    def post(self, token_data):
        '''Create hotel'''
        hotel = Hotel.from_document(api.payload)
        hotel.created_at = datetime.utcnow()
        return hotel.save(), 201
