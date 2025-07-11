from app import create_app,db
from app.models import Mechanics,ServiceTickets
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')  
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        
        
    def test_create_mechanic(self):
        self.mechanic_payload = {
            "name": "matt",
            "experiance":4 
        }
     
        response = self.client.post('/mechanics/', json=self.mechanic_payload)
        self.assertEqual(response.status_code, 201)

        data = response.get_json()
        mechanic_data = data["mechanic"]
        self.assertEqual(mechanic_data["name"], self.mechanic_payload["name"])
        self.assertEqual(mechanic_data["experiance"], self.mechanic_payload["experiance"])
     
     
    def test_get_mechanics(self):
       
        db.session.query(Mechanics).delete()
        db.session.commit()

        item1 = Mechanics(name="amy",experiance=99)
        item2 = Mechanics(name="sona",experiance=7)
        db.session.add_all([item1, item2])
        db.session.commit()

       
        response = self.client.get("/mechanics/")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        item_names = [item["name"] for item in data]
        self.assertIn("sona", item_names)
        self.assertIn("amy", item_names)
        
    def test_get_mechanic_by_id(self):
       
        item = Mechanics(name="sona",experiance=7)
        db.session.add(item)
        db.session.commit()

       
        response = self.client.get(f"/mechanics/{item.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["name"], "sona")
        self.assertEqual(data["experiance"], 7)
            
        
    def test_delete_mechanic(self):
        mechanic = Mechanics(name="matt",experiance=4)
        db.session.add(mechanic)
        db.session.commit()
        response = self.client.delete(f'/mechanics/{mechanic.id}')
        self.assertEqual(response.status_code, 200)
    
        deleted = db.session.get(Mechanics, mechanic.id)
        self.assertIsNone(deleted)
        
    
    def test_update_mechanic_success(self):
       
        item = Mechanics(name="sona",experiance=8)
        db.session.add(item)
        db.session.commit()

        update_payload = {
            "name": "sona",
            "experiance": 8
        }

        response = self.client.put(f"/mechanics/{item.id}", json=update_payload)
        self.assertEqual(response.status_code, 200)

        updated = response.get_json()
        self.assertEqual(updated["name"], update_payload["name"])
        self.assertEqual(updated["experiance"], update_payload["experiance"])
        
        
    def test_mechanic_experiance_sorting(self):
        # Setup: create mechanics and services
        m1 = Mechanics(name="Maya", experiance=3)
        m2 = Mechanics(name="Leo", experiance=6)
        m3 = Mechanics(name="Sophie", experiance=4)

        s1 = ServiceTickets(mileage=40000, VIN="AAA111", customer_id=13)
        s2 = ServiceTickets(mileage=50000, VIN="BBB222", customer_id=15)
        s3 = ServiceTickets(mileage=60000, VIN="CCC333", customer_id=16)

        db.session.add_all([m1, m2, m3, s1, s2, s3])
        db.session.commit()

        # Link mechanics to services
        s1.mechanics.append(m1)       # 1 service
        s2.mechanics.extend([m1, m2]) # m1 now has 2, m2 has 1
        s3.mechanics.append(m2)       # m2 now has 2 total
        db.session.commit()

        response = self.client.get("/mechanics/experiance")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 5)

        # Validate order: m2 (2 services), m1 (2 services), m3 (0 services)
        sorted_names = [mech["name"] for mech in data]
        self.assertIn("Maya", sorted_names)
        self.assertIn("Leo", sorted_names)
        self.assertIn("Sophie", sorted_names)

        service_counts = [len(mech["service"]) for mech in data]
        self.assertTrue(service_counts[0] >= service_counts[1])
        self.assertTrue(service_counts[1] >= service_counts[2])
        
        
    def test_search_mechanics_by_name(self):
        # Setup: add some mechanics
        m1 = Mechanics(name="Alice", experiance=5)
        m2 = Mechanics(name="Alfred", experiance=3)
        m3 = Mechanics(name="Bob", experiance=7)
        db.session.add_all([m1, m2, m3])
        db.session.commit()

        # Search for mechanics with name containing 'Al'
        response = self.client.get("/mechanics/search?name=Al")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 2)

        matched_names = [mech["name"] for mech in data]
        self.assertIn("Alice", matched_names)
        self.assertIn("Alfred", matched_names)
        self.assertNotIn("Bob", matched_names)

