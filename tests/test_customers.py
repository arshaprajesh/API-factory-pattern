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
        
        
        
        self.customer_payload = {
            "name": "Jane",
            "email": "ad@gmail.com",
            "address": "123 Maple St",
            "phone": "123-456-7890",
            "salary": 75000
        }
        self.customer = Customer(**self.customer_payload, password="456767")
        db.session.add(self.customer)
        db.session.commit()
        self.token = encode_token(self.customer.id)
    
    
    def test_create_customer(self):
        response = self.client.post('/customers/', json=self.customer_payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        if response.status_code != 201:
            print("Unexpected response:", data)
        else:
            self.assertEqual(data['email'], self.customer_payload['email'])
            
        
    def test_get_customer_by_id(self):
        response = self.client.get(f'/customers/{self.customer.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], self.customer.email)
        
        
    def test_paginated_customers(self):
        response = self.client.get("/customers?page=1&per_page=2", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        names = [cust["name"] for cust in data]
        self.assertIn("Jane", names)
         
    def tearDown(self):
        db.session.remove() # Remove the session to prevent lingering connections
        db.drop_all()       # Drop all tables to clean up the test database
        self.app_context.pop() 
               
    def test_login_customer(self):
        self.login_payload = {
            "email": "ad@gmail.com",
            "password": "456767"
        }
        print("json data:",self.login_payload)
        response = self.client.post('/customers/login', json=self.login_payload)
        print("response:",response.status_code)
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        print("Response JSON:", response.get_json())
        
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Login successful')
        self.assertIn('token', data)
        return data['token']  
     
    
    def test_login_customer_invalid(self):
        self.login_payload = {
            "email": "ad@gmail.com",
            "password": "7898"
        }
        response = self.client.post('/customers/login', json=self.login_payload)
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        print("Response JSON:", response.get_json())
        
        self.assertEqual(data['message'], 'invalid username or password') 
             
    
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
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Peter')
        self.assertEqual(data['email'], '')
         
     
    def test_delete_customer_success(self):
        token = encode_token(self.customer.id)
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.delete(f"/customers/",headers=headers)
        print("Delete response:", response.status_code)
        print("Delete JSON:", response.get_json())  
        
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("successfully deleted", data["message"])
       
        
        # Confirm deletion
        deleted = db.session.get(Customer, self.customer.id)
        self.assertIsNone(deleted)   