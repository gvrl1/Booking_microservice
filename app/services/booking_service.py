from app.models import Booking
from app.repositories import BookingRepository
from app.mapping import UserSchema, ApartmentSchema
from app import cache
import requests

booking_repository = BookingRepository()
user_schema = UserSchema()
apartment_schema = ApartmentSchema()

class BookingService:
    """
    En este servicio van todas las funciones referidas a la reserva.
    Buscar todas las reservas, buscar una reserva por id, crear una reserva.
    """

    def create(self, entity: Booking, user_id: int, apartment_id: int) -> Booking:
        user_request = requests.get("http://services-user-1:5000/api/v1/user/findbyid/{}".format(user_id))
        apartment_request = requests.get("http://services-apartment-1:5000/api/v1/apartment/findbyid/{}".format(apartment_id))
        user = user_schema.load(user_request.json()['data']['User'])
        apartment = apartment_schema.load(apartment_request.json()['data']['apartment'])
        entity.user_id = user.id
        entity.apartment_id = apartment.id
        booking = booking_repository.create(entity)
        cache.set(f"{booking.id}", booking, timeout=50)
        return booking
    
    @cache.memoize(timeout=50)
    def find_all(self) -> list:
        return booking_repository.find_all()
    
    def find_by_id(self, id: int) -> Booking:
        booking = cache.get(f"{id}")
        if booking is None:
            booking = booking_repository.find_by_id(id)
            if not booking:
                return None
            cache.set(f"{booking.id}", booking, timeout=50)
        return booking
    
    def update(self, entity: Booking, id: int) -> Booking:
        booking = cache.get(f"{id}")
        if booking:
            cache.update(f"{id}", entity, timeout=50)
            booking = booking_repository.update(entity, id)
        else:
            booking = booking_repository.update(entity, id)
            cache.set(f"{booking.id}", booking, timeout=50)
        return booking