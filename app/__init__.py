from flask import Flask
from .extensions import ma,limiter,cache 
from .models import db
from .bluePrints.customers import customers_bp
from .bluePrints.mechanics import mechanics_bp
from .bluePrints.serviceTickets import serviceTickets_bp
from .bluePrints.inventory import inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS 
from flask import send_from_directory

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'https://api-factory-pattern.onrender.com/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "mechanic_service"
    }
)

def create_app(config_name):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

  
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        response = send_from_directory('static', filename)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

   
    app.config.from_object('config.' + config_name)
    
    #=====initialize extensions=======
    ma.init_app(app)
    db.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    #=============================
    CORS(customers_bp)
    CORS(mechanics_bp)
    CORS(serviceTickets_bp)
    CORS(inventory_bp)
    
     #=====register blue prints=======
    app.register_blueprint(customers_bp,url_prefix = '/customers')
    app.register_blueprint(mechanics_bp,url_prefix = '/mechanics')
    app.register_blueprint(serviceTickets_bp,url_prefix = '/service')
    app.register_blueprint(inventory_bp,url_prefix = '/inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint
    
  
   
     
    return app
    