from .schemas import inventory_schema,inventories_schema
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Inventory,db
from . import inventory_bp



@inventory_bp.route("/",methods=['POST'])
def create_inventory():
    try:
        inventory_data=inventory_schema.load(request.json)
        print("inventory_data:",inventory_data)
    except ValidationError as e:
        return jsonify({"errors":e.messages,"invalid_data":request.json}),400
    
    new_inventory=Inventory(**inventory_data)
   
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory),201 

#=======get inventories=====
 
@inventory_bp.route("/", methods=['GET', 'OPTIONS'])
def get_inventoris():
    query = select(Inventory)
    inventories = db.session.execute(query).scalars().all() 
    return inventories_schema.jsonify(inventories),200 



#=======get specific inventory=====

@inventory_bp.route("/<int:id>", methods=['GET'])
def get_inventory(id):
    inventory = db.session.get(Inventory, id)

    if inventory:
        return inventory_schema.jsonify(inventory), 200
    return jsonify({"error": "inventory not found."}), 400

#============UPDATE SPECIFIC inventory===========

@inventory_bp.route("/<int:id>", methods=['PUT'])
def update_inventory(id):
    inventory = db.session.get(Inventory, id)

    if not inventory:
        return jsonify({"error": "inventory not found."}), 400
    
    try:
        inventory_data = inventory_schema.load(request.json)
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 415
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


#============DELETE SPECIFIC inventory===========

@inventory_bp.route("/<int:id>", methods=['DELETE'])
def delete_inventory(id):
    query=select(Inventory).where(Inventory.id==id)
    inventory=db.session.execute(query).scalars().first()
    
    db.session.delete(inventory)
    db.session.commit()
    return jsonify({"message": f'inventory id: {id}, successfully deleted.'}), 200
     
     
