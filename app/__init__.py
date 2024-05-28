from flask import Flask, app
import os
from app.config import config
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache()

def create_app():
    app = Flask(__name__)

    config_name = os.getenv('FLASK_ENV')

    f = config.factory(config_name if config_name else 'development')
    app.config.from_object(f)

    f.init_app(app)
    db.init_app(app)

    cache.init_app(app, config={'CACHE_TYPE': 'RedisCache', 'CACHE_DEFAULT_TIMEOUT': 300, 'CACHE_REDIS_HOST': 'redis.um.localhost', 'CACHE_REDIS_PORT':'6379', 'CACHE_REDIS_DB': '0', 'CACHE_REDIS_PASSWORD': '12345', 'CACHE_KEY_PREFIX': 'booking_'})

    from app.resources import booking
    app.register_blueprint(booking, url_prefix='/api/v1/booking')

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
   
    return app