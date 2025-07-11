from .schemas import customer_schema,customers_schema#,login_schema
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer,db
from . import customers_bp
from app.extensions import limiter

from app.utils.util import encode_token,token_required

@customers_bp.route("/login",methods=['POST'])
def login():
    try:
        credentials = request.json
        username = credentials['email']
        password = credentials['password']
    except ValidationError as e:
        return jsonify(e.messages),400
    
    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(query).scalars().first()  
    
    if customer and Customer.password == password:
        token = encode_token(customer.id)
        
        response = {    
            "status":"success",
            "message":"Login successful",
            "token": token
        }
        
        return jsonify(response),200
    else:
        return jsonify({"message":"invalid username or password"}),401
        

@customers_bp.route("/",methods=['POST'])
@limiter.limit("5 per day") #limit this request to add 5 customer per day
def create_customer():
    print("create customer")
    try:
        customer_data=customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify({"errors":e.messages,"invalid_data":request.json}),400
    
    query=select(Customer).where(Customer.email == customer_data['email'])
    existing_customer=db.session.execute(query).scalars().all()
    if existing_customer:
        return jsonify({"error":"Email already associated with an account"}),400
    
    new_customer=Customer(**customer_data)
    #new_customer = Customer(name=customer_data['name'], email=customer_data['email'], address=customer_data['address'],phone=customer_data['phone'],salary=customer_data['salary'])
   
    db.session.add(new_customer)
    db.session.commit()
    return jsonify(customer_schema.dump(new_customer)),201 

#=======get customer=====
"""  
@customers_bp.route("/", methods=['GET'])
@cache.cached(timeout=20)
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all() #Exectute query, and convert row objects into scalar objects (python useable)
   
    return customers_schema.jsonify(customers),200 """


#==================get customer using pagination ===========================

@customers_bp.route("/", methods=['GET'])
def get_customer_pages():
    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customer =db.paginate(query, page=page, per_page=per_page)
        
        return customers_schema.jsonify(customer),200
    except:   
        query = select(Customer)
        customers = db.session.execute(query).scalars().all() 
        
        return customers_schema.jsonify(customers),200

#=======get specific customer=====

@customers_bp.route("/<int:id>", methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 400

#============UPDATE SPECIFIC customer===========

@customers_bp.route("/", methods=['PUT'])
@token_required
def update_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "customer not found."}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    """ for key, value in customer_data.items():
        setattr(customer, key, value) """
    for key in request.json:
        setattr(customer, key, request.json[key])
    db.session.commit()
    return customer_schema.jsonify(customer), 200

#============DELETE SPECIFIC customer===========

@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(id):
    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"error": "customer not found."}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'customer id: {id}, successfully deleted.'}), 200 

#============DELETE SPECIFIC customer(otherway)===========
"""  
@customers_bp.route("/", methods=['DELETE'])
@token_required
def delete_customer(id):
    query=select(Customer).where(Customer.id==id)
    customer=db.session.execute(query).scalars().first()
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'customer id: {id}, successfully deleted.'}), 200"""
     