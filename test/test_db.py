import unittest
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db

class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # test connection to db
    def test_db_connection(self):
        connection = psycopg2.connect(dbname=os.getenv('DB_NAME'),
                                     user=os.getenv('DB_USER'),
                                     password=os.getenv('DB_PASSWORD'),
                                     host=os.getenv('DB_HOST'),
                                     port=os.getenv('DB_PORT'))
        self.assertTrue(connection)
