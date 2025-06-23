from flask import Flask
from .extensions import ma,limiter,cache 
from .models import db
from .bluePrints.customers import customers_bp
from .bluePrints.mechanics import mechanics_bp
from .bluePrints.serviceTickets import serviceTickets_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_name}')
    
    #=====initialize extensions=======
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
     #=====register blue prints=======
    app.register_blueprint(customers_bp,url_prefix = '/customers')
    app.register_blueprint(mechanics_bp,url_prefix = '/mechanics')
    app.register_blueprint(serviceTickets_bp,url_prefix = '/service')
    
     
    return app
    