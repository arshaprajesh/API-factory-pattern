
""" from app import create_app
from app.models import db
import os

app = create_app('ProductionConfig')

with app.app_context():
    #db.drop_all() 
    db.create_all() 
    



 """
from app import create_app
from app.models import db
import os

config_name = os.environ.get('FLASK_CONFIG', 'ProductionConfig')
app = create_app(config_name)

with app.app_context():
   
    # db.drop_all()
    db.create_all()



        