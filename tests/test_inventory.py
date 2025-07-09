from app import create_app,db
from app.models import Inventory
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')  
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        
    def test_create_inventory(self):
        self.inventory_payload = {
            "name": "Battery",
            "price":455.00 
        }
     
        response = self.client.post('/inventory/', json=self.inventory_payload)
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        self.assertEqual(data["name"], self.inventory_payload["name"])
        self.assertEqual(data["price"], self.inventory_payload["price"])
     
     
    
        
    def test_delete_inventory(self):
        inventory = Inventory(name="Shock Absorber",price=49.99)
        db.session.add(inventory)
        db.session.commit()
        response = self.client.delete(f'/inventory/{inventory.id}')
        self.assertEqual(response.status_code, 200)
    
        deleted = db.session.get(Inventory, inventory.id)
        self.assertIsNone(deleted)
        
    def test_get_inventories(self):
       
        db.session.query(Inventory).delete()
        db.session.commit()

        item1 = Inventory(name="Brake Pads",price=19.99)
        item2 = Inventory(name="Headlight Bulb",price=7.50)
        db.session.add_all([item1, item2])
        db.session.commit()

       
        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        item_names = [item["name"] for item in data]
        self.assertIn("Brake Pads", item_names)
        self.assertIn("Headlight Bulb", item_names)
        
    def test_get_inventory_by_id(self):
       
        item = Inventory(name="Timing Belt",price=49.95)
        db.session.add(item)
        db.session.commit()

       
        response = self.client.get(f"/inventory/{item.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "Timing Belt")
        self.assertEqual(data["price"], 49.95)
            
    def test_update_inventory_success(self):
       
        item = Inventory(name="Air Filter",price=8.99)
        db.session.add(item)
        db.session.commit()

        update_payload = {
            "name": "Premium Air Filter",
            "price": 9.49
        }

        response = self.client.put(f"/inventory/{item.id}", json=update_payload)
        self.assertEqual(response.status_code, 200)

        updated = response.get_json()
        self.assertEqual(updated["name"], update_payload["name"])
        self.assertEqual(updated["price"], update_payload["price"])
        

        