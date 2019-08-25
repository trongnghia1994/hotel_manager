from datetime import datetime

from flask_restplus import Namespace, Resource, fields

from core.models.accommodation import Accommodation
from decorators import login_required
from common import authorizations

api = Namespace('accommodation', description='Accomodation related operations', authorizations=authorizations)

accommodation_fields = api.model('Accommodation', {
    '_id': fields.String(readonly=True),
    'hotel_id': fields.String(required=True, example="5d5ff40668a3ff060c2df835"),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'max_guests': fields.Integer(required=True, example=5),
})


@api.doc(security='authToken')
@api.route('/')
class AccommodationResource(Resource):
    @api.expect(accommodation_fields, validate=True)
    @login_required('accommodation.add')
    @api.marshal_with(accommodation_fields, code=201, mask='_id')
    def post(self, token_data):
        '''Create accommodation'''
        accommodation = Accommodation.from_document(api.payload)
        accommodation.created_at = datetime.utcnow()
        return accommodation.save(), 201
