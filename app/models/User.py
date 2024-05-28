from app import db
from dataclasses import dataclass

@dataclass
class User(db.Model): 
    __tablename__ ='users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(100))
    lastname = db.Column('lastname', db.String(100))
    phone_number = db.Column('phone_number', db.String(15))
    email_address = db.Column('email_address', db.String(100), unique=True)
    password = db.Column('password', db.String(255))
