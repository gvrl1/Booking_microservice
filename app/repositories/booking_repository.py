from app.models import Booking
from app import db
from app.repositories.repository_base import Create, Read, Update


class BookingRepository(Create, Read, Update):
    
    def create(self, entity: Booking) -> Booking:
        db.session.add(entity)
        db.session.commit()
        return entity
        
    def find_all(self) -> list:
        return db.session.query(Booking).all()
    
    def find_by_id(self, id: int) -> Booking:
        return Booking.query.get(id)
    
    def update(self, Booking: Booking, id: int) -> Booking:
        entity = self.find_by_id(id)
        entity.start_booking = Booking.start_booking
        entity.finish_booking = Booking.finish_booking
        entity.duration = Booking.duration
        entity.amount_people = Booking.amount_people
        db.session.add(entity)
        db.session.commit()
        return entity