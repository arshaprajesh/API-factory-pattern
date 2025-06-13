from app.extensions import ma
from app.models import ServiceTickets

class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
     model = ServiceTickets
     include_fk=True#Need this because Auto Schemas don't automatically recognize foreign keys (customer_id) 

 
service_schema = ServiceTicketsSchema()
services_schema = ServiceTicketsSchema(many= True)