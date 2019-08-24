import os

from flask import Flask
from pymodm import connect

from apiv1 import blueprint as api1
from config import DevConfig, ProdConfig


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api1)
    config = ProdConfig if os.getenv('APP_IS_PROD') else DevConfig
    app.config.from_object(config)
    connect(app.config['MONGODB_URI'], connect=False)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
