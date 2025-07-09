from app import create_app,db
from app.models import ServiceTickets,Mechanics,Inventory
import unittest

class TestService(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')  
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        
    def test_create_service(self):
       
        self.service_payload = {
            "mileage": 45000,
            "VIN":"va657" ,
            "customer_id":20
        }
        
        response = self.client.post('/service/', json=self.service_payload)
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        service_data = data["service"]
        self.assertEqual(service_data["mileage"], int(self.service_payload["mileage"]))
        self.assertEqual(service_data["VIN"], self.service_payload["VIN"])
        self.assertEqual(service_data["customer_id"], self.service_payload["customer_id"])
     
    def test_get_services(self):
       
        db.session.query(ServiceTickets).delete()
        db.session.commit()

        service1 = ServiceTickets(mileage=45000,VIN="19sta",customer_id=20)
        service2 = ServiceTickets(mileage=35000,VIN="17865",customer_id=18)
        db.session.add_all([service1, service2])
        db.session.commit()

       
        response = self.client.get("/service/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        service_list = [service["VIN"] for service in data]
        self.assertIn("19sta", service_list)
        self.assertIn("17865", service_list)
        
    def test_get_service_by_id(self):
       
        service = ServiceTickets(mileage=35000,VIN="19sta",customer_id=20)
        db.session.add(service)
        db.session.commit()

       
        response = self.client.get(f"/service/{service.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["mileage"], 35000)
        self.assertEqual(data["VIN"], "19sta") 
        self.assertEqual(data["customer_id"], 20) 
    
    def test_delete_service_success(self):
    
        service = ServiceTickets(mileage=50000, VIN="X123YZ", customer_id=18)
        db.session.add(service)
        db.session.commit()

       
        response = self.client.delete(f"/service/{service.id}")
        self.assertEqual(response.status_code, 200)

       
        data = response.get_json()
        self.assertIn("message", data)
        self.assertTrue(f"service id: {service.id}" in data["message"])

        deleted = db.session.get(ServiceTickets, service.id)
        self.assertIsNone(deleted)    
    
    
    def test_edit_service_mechanics(self):
        
        service = ServiceTickets(mileage=60000, VIN="ABC123", customer_id=18)
        mechanic1 = Mechanics(name="Alice", experiance=5)
        mechanic2 = Mechanics(name="Bob", experiance=7)
        mechanic3 = Mechanics(name="Charlie", experiance=8)
        db.session.add_all([service, mechanic1, mechanic2, mechanic3])
        db.session.commit()

        # Pre-associate mechanic2
        service.mechanics.append(mechanic2)
        db.session.commit()

        # Update payload: add mechanic1, remove mechanic2
        payload = {
            "add_mechanic_ids": [mechanic1.id],
            "remove_mechanic_ids": [mechanic2.id]
        }

        response = self.client.put(f"/service/{service.id}", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        print("Edit response JSON:", response.get_json())
        mechanic_ids = [m["id"] for m in data["mechanics"]]  # assumes schema includes 'mechanics' list
        print("mechanic_ids:", mechanic_ids)

        self.assertIn(mechanic1.id, mechanic_ids)
        self.assertNotIn(mechanic2.id, mechanic_ids)
        self.assertNotIn(mechanic3.id, mechanic_ids)  # not touched
    
    
    
    
    def test_add_mechanic_to_service_success(self):
        service = ServiceTickets(mileage=65000, VIN="Z456LM", customer_id=17)
        mechanic = Mechanics(name="Derek", experiance=6)
        db.session.add_all([service, mechanic])
        db.session.commit()

        response = self.client.put(f"/service/{service.id}/add_mechanic/{mechanic.id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["Message"], "Successfully added mechanic to service.")
        self.assertIn(mechanic, service.mechanics)
        
    
    
    def test_remove_mechanic_success(self):
        service = ServiceTickets(mileage=75000, VIN="LMNOP", customer_id=17)
        mechanic = Mechanics(name="Sam", experiance=4)

        db.session.add_all([service, mechanic])
        db.session.commit()

        service.mechanics.append(mechanic)
        db.session.commit()

        response = self.client.put(f"/service/{service.id}/remove_mechanic/{mechanic.id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["message"], "successfully removed mechanic to service")
        self.assertNotIn(mechanic, service.mechanics)   
        
        
    def test_add_inventory_success(self):
        service = ServiceTickets(mileage=82000, VIN="T1Z9QW", customer_id=20)
        inventory = Inventory(name="Radiator Hose", price=150.99)

        db.session.add_all([service, inventory])
        db.session.commit()

        response = self.client.put(f"/service/{service.id}/add_inventory/{inventory.id}")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["Message"], "Successfully added inventory to service.")
        self.assertIn(inventory, service.inventories)