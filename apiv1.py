from flask import Blueprint
from flask_restplus import Api

from apis.accommodation import api as accommodation
from apis.auth import api as auth
from apis.hotel import api as hotel
from apis.reservation import api as reservation
from apis.room_inventory import api as room_inventory

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint,
          title='API',
          version='1.0',
          description='RESTFul API web services',
          doc='/docs'
          )

api.add_namespace(auth, path='/auth')
api.add_namespace(reservation, path='/reservations')
api.add_namespace(accommodation, path='/accommodations')
api.add_namespace(hotel, path='/hotels')
api.add_namespace(room_inventory, path='/roomInventories')
