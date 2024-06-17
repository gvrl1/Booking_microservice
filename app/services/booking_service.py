from app.models import Booking
from app.repositories import BookingRepository
from app.mapping import UserSchema, ApartmentSchema
from app import cache
from tenacity import retry, wait_random, stop_after_attempt
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
        try:
            user_request = self.get_user(user_id)
            apartment_request = self.get_apartment(apartment_id)
            if not user_request or not apartment_request:
                return None
        except:
            return None
        user = user_schema.load(user_request.json()['data']['User'])
        apartment = apartment_schema.load(apartment_request.json()['data']['apartment'])
        entity.user_id = user.id
        entity.apartment_id = apartment.id
        booking = booking_repository.create(entity)
        cache.set(f"{booking.id}", booking, timeout=50)
        return booking

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=3))
    def get_apartment(self, apartment_id):
        apartment = cache.get(f"apartment_{apartment_id}")
        if apartment is None:
            apartment = requests.get("http://apartment.um.localhost:5000/api/v1/apartment/findbyid/{}".format(apartment_id))
            if apartment.status_code != 200:
                return None
            cache.set(f"apartment_{apartment_id}", apartment, timeout=50)
        return apartment

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=3))
    def get_user(self, user_id):
        user = cache.get(f"user_{user_id}")
        if user is None:
            user = requests.get("http://user.um.localhost:5000/api/v1/user/findbyid/{}".format(user_id))
            if user.status_code != 200:
                return None
            cache.set(f"user_{user_id}", user, timeout=50)
        return user
    
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