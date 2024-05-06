from app.models import Booking
from app.repositories import BookingRepository
import requests


class BookingService:
    """
    En este servicio van todas las funciones referidas a la reserva.
    Buscar todas las reservas, buscar una reserva por id, crear una reserva.
    """
    def __init__(self):
        self.__repo = BookingRepository()

    def create(self, entity: Booking, user_id: int, apartment_id: int) -> Booking:
        user = requests.get("http://localhost:5000/api/v1/user/findbyid/{}".format(user_id))
        apartment = requests.get("http://localhost:5000/api/v1/apartment/findbyid/{}".format(apartment_id))
        entity.user = user
        entity.apartment = apartment
        return self.__repo.create(entity)
    
    def find_all(self) -> list:
        return self.__repo.find_all()
    
    def find_by_id(self, id: int) -> Booking:
        return self.__repo.find_by_id(id)
    
    def update(self, entity: Booking, id: int) -> Booking:
        return self.__repo.update(entity, id)