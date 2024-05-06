import unittest
from app import create_app, db
from app.models import Booking
from app.services import BookingService

booking_service = BookingService()

class BookingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_entity(self):
        entity = Booking(
            user_id=1,
            apartment_id=1,
            start_date='2021-07-01',
            finish_date='2021-07-10',
            duration=9,
            amount_people=2
        )
        booking_service.create(entity)
        return entity
    
    def test_create_booking(self):
        entity = self.create_entity()
        self.assertTrue(entity.id)

    def test_find_by_id_booking(self):
        entity = self.create_entity()
        self.assertIsNone(booking_service.find_by_id(entity.id))

    def test_find_all_booking(self):
        entity = self.create_entity()
        self.assertTrue(booking_service.find_all())

    def test_update_booking(self):
        entity = self.create_entity()
        entity.amount_people = 3
        booking_service.update(entity, entity.id)
        self.assertEqual(booking_service.find_by_id(entity.id).amount_people, 3)

if __name__ == '__main__':
    unittest.main()