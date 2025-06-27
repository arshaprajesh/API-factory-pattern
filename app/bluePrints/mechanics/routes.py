from .schemas import mechanic_schema,mechanics_schema
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Mechanics,db
from app.extensions import cache
from . import mechanics_bp



@mechanics_bp.route("/",methods=['POST'])
def create_mechanic():
    try:
        mechanic_data=mechanic_schema.load(request.json)
        
    except ValidationError as e:
        return jsonify({"errors":e.messages,"invalid_data":request.json}),400
    
    new_mechanic=Mechanics(**mechanic_data)
   
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify({"message":"new mechanic added","mechanic":mechanic_schema.dump(new_mechanic)}),201 

#=======get mechanics=====

@mechanics_bp.route("/", methods=['GET'])
@cache.cached(timeout=20)
def get_mechanics():
    query = select(Mechanics)
    result = db.session.execute(query).scalars() #Exectute query, and convert row objects into scalar objects (python useable)
    mechanics = result.all() #packs objects into a list
    return mechanics_schema.jsonify(mechanics),200

#=======get specific mechanic=====
 
@mechanics_bp.route("/<int:id>", methods=['GET'])
def get_mechanic(id):
    mechanic = db.session.get(Mechanics, id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic), 400
    return jsonify({"error": "Mechanic not found."}), 400 

#============UPDATE SPECIFIC mechanic===========

@mechanics_bp.route("/<int:id>", methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanics, id)
    if not mechanic:
        return jsonify({"error": "mechanic not found."}), 400
    
    try:
        mechanic_data = mechanic_schema.load(request.json)
        
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
     #mechanic.name = mechanic_data['name'] 
    #mechanic.experiance = mechanic_data['experiance'] 

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200

#============DELETE SPECIFIC mechanic===========

@mechanics_bp.route("/<int:id>", methods=['DELETE'])
def delete_mechanic(id):
    print("going to delete customer")   
    mechanic = db.session.get(Mechanics, id)

    if not mechanic:
        return jsonify({"error": "invalid mechanic id."}), 400
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"mechanic id: {id}, successfully deleted."}), 200

#========================get mechanics in sorting(using lambda)=====
#======================MECHANIC WHO HAS WORKED ON MOST TICKET================

@mechanics_bp.route("/experiance", methods=['GET'])
def mechanic_experiance():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics.sort(key= lambda mechanic: len(mechanic.service),reverse = True)
    
    return mechanics_schema.jsonify(mechanics) 

#========================get mechanics name (with specific letter or letters)==================

@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name=request.args.get("name")
    
    query = select(Mechanics).where(Mechanics.name.like(f'%{name}%'))
    mechanics =db.session.execute(query).scalars().all()
    
    return mechanics_schema.jsonify(mechanics)

