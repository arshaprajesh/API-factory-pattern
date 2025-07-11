from app.extensions import ma
from app.models import Mechanics
from marshmallow import fields


class MechanicSchema(ma.SQLAlchemyAutoSchema): 
    service = fields.Nested("ServiceTicketsSchema")
    class Meta:
     model = Mechanics
     

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many= True)
