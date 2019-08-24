from flask import Config


class BaseConfig(Config):
    DEBUG = True


class DevConfig(Config):
    DEBUG = True
    MONGODB_URI = 'mongodb://admin:ZeLGzN1WJ365Y6eq@beagreatcluster-shard-00-00-nzdwh.mongodb.net:27017,beagreatcluster-shard-00-01-nzdwh.mongodb.net:27017,beagreatcluster-shard-00-02-nzdwh.mongodb.net:27017/test?ssl=true&replicaSet=BeagreatCluster-shard-0&authSource=admin&retryWrites=true&w=majority'
    SECRET_KEY = 'A very secret key'


class ProdConfig(Config):
    DEBUG = True
    MONGODB_URI = 'mongodb://admin:ZeLGzN1WJ365Y6eq@beagreatcluster-shard-00-00-nzdwh.mongodb.net:27017,beagreatcluster-shard-00-01-nzdwh.mongodb.net:27017,beagreatcluster-shard-00-02-nzdwh.mongodb.net:27017/test?ssl=true&replicaSet=BeagreatCluster-shard-0&authSource=admin&retryWrites=true&w=majority'
    SECRET_KEY = 'A very secret key'
