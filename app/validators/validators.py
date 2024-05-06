from flask import jsonify, request
from functools import wraps

from marshmallow import ValidationError

def validate_with(schema):
    """
    Se encarga de validar el request con el schema que recibe por parámetro.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = schema().load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400
            return f(data, *args, **kwargs)
        return decorated_function
    return decorator


def validate_exists(service, response):
    """
    Se encarga de validar que el objeto exista en la base de datos.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id = kwargs.get('id')
            if id is None and len(args) > 1:
                id = args[1]
            if not service.find_by_id(id):
                response.add_status_code(400).add_message("Whatever you're looking for, it doesn't exist.").add_data()
                return jsonify(response.build()), response.status_code
            return f(*args, **kwargs)
        return decorated_function
    return decorator