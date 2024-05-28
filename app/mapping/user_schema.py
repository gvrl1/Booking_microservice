from app.models import User
from marshmallow import validate, fields, Schema, post_load

class UserSchema(Schema):
    # TODO: Habrá que ver que datos interesa enviar en el JSON
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    lastname = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone_number = fields.Str(required=True, validate=validate.Length(min=1, max=15))
    email_address = fields.Str(required=True, validate=validate.Email())
    password = fields.Str(load_only=True)
    data = fields.Nested('UserDataSchema')
    
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)