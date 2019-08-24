from datetime import datetime

from flask_restplus import Namespace, Resource, fields

from core.models.hotel import Hotel

api = Namespace('hotel', description='Hotel related operations')

hotel_fields = api.model('Hotel', {
    '_id': fields.String(readonly=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'timezone': fields.String(required=True),
    'currency': fields.String(required=True),
    'address': fields.String(required=True),
    'website': fields.String(required=True),
    'logo_url': fields.String(readonly=True),
    'cover_url': fields.String(readonly=True),
    'loyalty_club': fields.String(readonly=True),
    'loyalty_url': fields.String(readonly=True),
    'created_at': fields.String(readonly=True),
    'updated_at': fields.String(readonly=True),
})


@api.route('/')
class HotelResource(Resource):
    @api.expect(hotel_fields, validate=True)
    @api.marshal_with(hotel_fields, code=201, mask='_id')
    def post(self):
        '''Create hotel'''
        hotel = Hotel.from_document(api.payload)
        hotel.created_at = datetime.utcnow()
        return hotel.save(), 201
