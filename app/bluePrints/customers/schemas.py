from app.extensions import ma
from app.models import Customer

from flask_marshmallow import Marshmallow
  
ma = Marshmallow()
  
class CustomerSchema(ma.SQLAlchemyAutoSchema): 
    class Meta:
     model = Customer
     load_instance = True


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many= True)
#login_schema = CustomerSchema(exclude = ['name','email'])


