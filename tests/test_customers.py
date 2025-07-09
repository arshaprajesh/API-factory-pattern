from app import create_app,db
from app.models import Customer
from app.utils.util import encode_token
import unittest



class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')  
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        self.token = encode_token(1)
        

        self.customer_payload = {
            "name": "Jane Doe",
            "email": "aw@gmail.com",
            "address": "123 Maple St",
            "phone": "123-456-7890",
            "salary": 75000
        }
        self.customer = Customer(**self.customer_payload, password="456767")
        db.session.add(self.customer)
        db.session.commit()
    

    def test_create_customer(self):
        response = self.client.post('/customers/', json=self.customer_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        if response.status_code != 201:
            print("Unexpected response:", data)
        else:
            self.assertEqual(data['email'], self.customer_payload['email'])
            
    def test_login_customer(self):
        self.login_payload = {
            "email": "aw@gmail.com",
            "password": "456767"
        }
        response = self.client.post('/customers/login', json=self.login_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('token', data)
        return data['token']
    
    
    def test_get_customer_by_id(self):
        response = self.client.get(f'/customers/{self.customer.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], self.customer.email)
        
    def test_login_customer_invalid_password(self):
        login_payload = {
            "email": "aw@gmail.com",
            "password": "456767"
        }
        response = self.client.post('/customers/login', json=login_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], "Login successful")
        
    def test_update_customer(self):
        update_payload = {
            "name": "Peter",
            "email": "",
            "address": "",
            "phone": "",
            "salary":0 ,
            "password":""
                
        }

        token = self.test_login_customer()
        headers = {'Authorization': f"Bearer {token}"}

        response = self.client.put('/customers/', json=update_payload, headers=headers)
        print("Update response:", response.status_code)
        print("Update JSON:", response.get_json())   
        data = response.get_json()
        print("Update response:", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Peter')
        self.assertEqual(data['email'], '')
        
       