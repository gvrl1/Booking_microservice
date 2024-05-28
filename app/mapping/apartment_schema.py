from app.models import Apartment
from marshmallow import validate, fields, Schema, post_load

class ApartmentSchema(Schema):
    id = fields.Int(dump_only=True)
    number_of_apartment = fields.Int(required=True, validate=validate.Range(min=1, max=999))
    size = fields.Int(required=True, validate=validate.Range(min=1, max=999))
    amount_rooms = fields.Int(required=True, validate=validate.Range(min=1, max=4))
    features = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    availability = fields.Bool(required=True)
    lease = fields.Float(required=True, validate=validate.Range(min=1, max=9999999999))
    address = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    data = fields.Nested('ApartmentDataSchema')

    @post_load
    def make_apartment(self, data, **kwargs):
        return Apartment(**data)