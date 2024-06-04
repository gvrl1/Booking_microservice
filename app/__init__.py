from flask import Flask
import os
from app.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
cache = Cache()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    config_name = os.getenv('FLASK_ENV')

    f = config.factory(config_name if config_name else 'development')
    app.config.from_object(f)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URI')

    f.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    redis_host = os.getenv('REDIS_HOST')
    redis_password = os.getenv('REDIS_PASSWORD')
    cache.init_app(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_DEFAULT_TIMEOUT': 300, 'CACHE_REDIS_HOST': redis_host, 'CACHE_REDIS_PORT':'6379', 'CACHE_REDIS_DB': '0', 'CACHE_REDIS_PASSWORD': redis_password, 'CACHE_KEY_PREFIX': 'booking_'})

    from app.resources import booking
    app.register_blueprint(booking, url_prefix='/api/v1/booking')

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
   
    return app