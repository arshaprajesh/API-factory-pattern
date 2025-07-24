
""" from app import create_app
from app.models import db
import os

app = create_app('ProductionConfig')

with app.app_context():
    #db.drop_all() 
    db.create_all() 
    
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


 """
from app import create_app
from app.models import db
import os

config_name = os.environ.get('FLASK_CONFIG', 'ProductionConfig')
app = create_app(config_name)

with app.app_context():
    # Only use this in dev/testing!
    # db.drop_all()
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

        