from dataclasses import dataclass
from app import db

@dataclass
class Apartment(db.Model):
    __tablename__ = 'apartments'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    number_of_apartment = db.Column('number_of_apartment', db.Integer)
    size = db.Column('size', db.Integer)
    amount_rooms = db.Column('amount_rooms',db.Integer)
    features = db.Column('features', db.String(500))
    availability = db.Column('availability',db.Boolean)
    lease = db.Column('lease', db.Float)
    address = db.Column('address', db.String(150))