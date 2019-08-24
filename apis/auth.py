from flask import request, session, current_app
from flask_restplus import Namespace, Resource, fields

from core.helpers.user_helper import login_user
from decorators import login_required
from common import authorizations

api = Namespace('auth', description='Auth related operations', authorizations=authorizations)

login_fields = api.model('Login', {
    'email': fields.String(required=True, description='User email to login', example="nghia@gmail.com"),
    'password': fields.String(required=True, description='User password', example="123456"),
})

login_resp_fields = api.model('LoginResponse', {
    'token': fields.String(required=True, description='User token to login', example="<jwt-token>"),
})


@api.route('/login')
@api.doc(responses={200: 'Success', 401: 'Unauthorized'})
class Login(Resource):
    @api.expect(login_fields, validate=True)
    @api.marshal_with(login_resp_fields)
    def post(self):
        '''Do login'''
        result = login_user(request.json)
        if not result:
            return 'Unauthorized', 401

        # Store user info on session
        session[result["user_id"]] = True
        current_app.logger.info('Session after login %s' % session)
        return {'token': result["token"]}, 200


@api.route('/logout')
@api.doc(security="authToken", responses={200: 'Success', 401: 'Unauthorized'})
class Logout(Resource):
    @login_required()
    def post(self, token_data):
        '''Do logout'''
        user_id = token_data['sub']
        session.pop(user_id, None)
        current_app.logger.info('Session after logout %s' % session)
        return 'Successfully', 200
