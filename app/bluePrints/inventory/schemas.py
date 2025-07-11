from app.extensions import ma
from app.models import Inventory
from marshmallow import fields

class InventorySchema(ma.SQLAlchemyAutoSchema): 
    service = fields.Nested("ServiceTicketsSchema")
    class Meta:
     model = Inventory


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many= True)

