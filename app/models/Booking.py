from dataclasses import dataclass
from app import db

@dataclass
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer)
    apartment_id = db.Column('apartment_id', db.Integer)
    start_date = db.Column('start_date', db.DateTime(100))
    finish_date = db.Column('finish_date',db.DateTime(100))
    duration = db.Column('duration', db.Integer)
    amount_people = db.Column('amount_people',db.Integer)