from app.models import Booking
from marshmallow import validate, fields, Schema, post_load


class BookingSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    apartment_id = fields.Int(dump_only=True)
    start_booking = fields.DateTime(required=True)
    finish_booking = fields.DateTime(required=True)
    duration = fields.Int(required=True, validate=validate.Range(min=1, max=30))
    amount_people = fields.Int(required=True, validate=validate.Range(min=1, max=10))
    data = fields.Nested('BookingDataSchema')

    @post_load
    def make_Booking(self, data, **kwargs):
        return Booking(**data)