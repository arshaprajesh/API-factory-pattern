
from app import create_app
from app.models import db
from sqlalchemy.dialects import registry
registry.register("postgresql.psycopg", "psycopg.sqlalchemy", "PsycopgDialect")

app = create_app('ProductionConfig')

with app.app_context():
    #db.drop_all() 
    db.create_all() 
    




        