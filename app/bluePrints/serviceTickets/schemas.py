from app.extensions import ma
from app.models import ServiceTickets
from marshmallow import fields

class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema): 
    mechanics = fields.Nested("MechanicSchema",many=True)
    customer = fields.Nested("CustomerSchema")
    class Meta:
        
        model = ServiceTickets
        #fields= ("service_ids","mileage","VIN","customer_id","serviceTickets","customer","id")
        include_fk=True #Need this because Auto Schemas don't automatically recognize foreign keys (customer_id) 
class EditServiceSchema(ma.Schema):
    
    add_mechanic_ids = fields.List(fields.Int(),required=True)
    remove_mechanic_ids = fields.List(fields.Int(),required=True)
    
    class meta:
        fields=("add_customer_ids","remove_customer_ids")
 
service_schema = ServiceTicketsSchema()
services_schema = ServiceTicketsSchema(many= True)
return_service_schema =ServiceTicketsSchema(exclude=["customer_id"])
edit_service_schema = EditServiceSchema()