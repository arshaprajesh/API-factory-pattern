from .schemas import customer_schema,customers_schema
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Customer,db
from . import customers_bp

@customers_bp.route("/customers",methods=['POST'])
def create_customer():
    print("create customer")
    try:
        print(request.json)
        customer_data=customer_schema.load(request.json)
        print("customer_data :",customer_data)
    except ValidationError as e:
        print("ValidationError",e.messages)
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

@customers_bp.route("/customers", methods=['GET'])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars() #Exectute query, and convert row objects into scalar objects (python useable)
    customers = result.all() #packs objects into a list
    return customers_schema.jsonify(customers),200

#=======get specific customer=====

@customers_bp.route("/customers/<int:id>", methods=['GET'])
def get_customer(id):
    customer = db.session.get(Customer, id)

    if customer:
        return customer_schema.jsonify(customer), 400
    return jsonify({"error": "Customer not found."}), 400

#============UPDATE SPECIFIC USER===========

@customers_bp.route("/customers/<int:id>", methods=['PUT'])
def update_customer(id):
    customer = db.session.get(Customer, id)

    if not customer:
        return jsonify({"error": "customer not found."}), 400
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

#============DELETE SPECIFIC USER===========

@customers_bp.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(id):
    customer = db.session.get(Customer, id)
    print("customer",customer)
    if not customer:
        return jsonify({"error": "customer not found."}), 400
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'customer id: {id}, successfully deleted.'}), 200