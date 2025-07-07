
from app import create_app
from app.models import db, Customer
from app.utils.util import encode_token
import unittest
from config import TestingConfig


class TestCustomer(unittest.TestCase):
    
    
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
    
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        
        
    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe", 
            "email": "jd@email.com", 
            "address": "cary", 
            "phone": "566 566 -6778", 
            "salary": 45000, 
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
        
        
    
    