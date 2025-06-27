from.schemas import service_schema,services_schema,edit_service_schema,return_service_schema
#from mechanics.schemas import mechanics_schema
from flask import request,jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTickets,db
from . import serviceTickets_bp
from app.models import Mechanics
from app.models import Inventory




@serviceTickets_bp.route("/",methods=['POST'])
def create_service():
    try:
        service_data=service_schema.load(request.json) 
    except ValidationError as e:
        return jsonify({"errors":e.messages,"invalid_data":request.json}),400
    
    new_service=ServiceTickets(**service_data)
    #new_service = ServiceTickets(VIN = service_data['VIN'],customer_id = service_data["customer_id"])
    
    db.session.add(new_service)
    db.session.commit()
    return jsonify({"message":"new service added","service":service_schema.dump(new_service)}),201 
     
#=======get service=====

@serviceTickets_bp.route("/", methods=['GET'])
def get_services():
    query = select(ServiceTickets)
    result = db.session.execute(query).scalars() #Exectute query, and convert row objects into scalar objects (python useable)
    service = result.all() #packs objects into a list
    return services_schema.jsonify(service),200

#=======get specific service=====

@serviceTickets_bp.route("/<int:id>", methods=['GET'])
def get_service(id):
    query=select(ServiceTickets).where(ServiceTickets.id ==id)
    result = db.session.execute(query).scalars().first()

    if result is None:
        return jsonify({"error": "service ticket not found"}), 400
    return service_schema.jsonify(result), 200

#============UPDATE SPECIFIC service===========
""" 
@serviceTickets_bp.route("/<int:id>", methods=['PUT'])
def update_service(id):
    service = db.session.get(ServiceTickets, id)

    if not service:
        return jsonify({"error": "service not found."}), 400
    
    try:
        service_data = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in service_data.items():
        setattr(service, key, value)

    db.session.commit()
    return service_schema.jsonify(service), 200 """

#============DELETE SPECIFIC service===========

@serviceTickets_bp.route("/<int:id>", methods=['DELETE'])
def delete_service(id):
    service = db.session.get(ServiceTickets, id)

    if not service:
        return jsonify({"error": "service not found."}), 400
    
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": f'service id: {id}, successfully deleted.'}), 200

#============EDIT SPECIFIC service===========

@serviceTickets_bp.route("/<int:service_id>", methods=['PUT'])
def edit_service(service_id):
    try:
        service_edits= edit_service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    
    query= select(ServiceTickets).where(ServiceTickets.id==service_id)
    service=db.session.execute(query).scalars().first()
    
    for mechanic_id in service_edits['add_mechanic_ids']:
        query= select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic=db.session.execute(query).scalars().first()
        
        if mechanic and mechanic not in service.mechanics:
            service.mechanics.append(mechanic)
            
    for mechanic_id in service_edits['remove_mechanic_ids']:
        query= select(Mechanics).where(Mechanics.id == mechanic_id)
        mechanic=db.session.execute(query).scalars().first()
        
        if mechanic and mechanic in service.mechanics:
            service.mechanics.remove(mechanic)
    
    db.session.commit()
    return return_service_schema.jsonify(service)
        
        
        

#==================ADD  mechanic to service===================

@serviceTickets_bp.route('/<int:service_id>/add_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic(service_id, mechanic_id):
    service = db.session.get(ServiceTickets, service_id) #can use .get when querying using Primary Key
    mechanic = db.session.get(Mechanics, mechanic_id)

    if service and mechanic: #check to see if both exist
        if mechanic not in service.mechanics: 
            service.mechanics.append(mechanic) 
            db.session.commit() 
            return jsonify({"Message": "Successfully added mechanic to service."}), 200
        else:
            return jsonify({"Message": "mechanic is already included in this service."}), 400
    else:
        return jsonify({"Message": "Invalid service id or mechanic id."}), 400
 

#==============REMOVE mechanic FROM service ==============

@serviceTickets_bp.route('/<service_id>/remove_mechanic/<mechanic_id>', methods=['PUT']) 

def remove_mechanic (service_id, mechanic_id): 

    service = db.session.get(ServiceTickets, service_id)  
    mechanic = db.session.get(Mechanics, mechanic_id) 

    if service and mechanic: 
        if  mechanic in service.mechanics: 
            service.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({
                "message":"successfully removed mechanic to service"}),200
        return jsonify({"error":"this mechanic is not in this service"})
        
    return jsonify({"message": "Invalid mechanic id or service id"}), 400 

#=======================REMOVE mechanic FROM service[delete]====================================

@serviceTickets_bp.route('/<service_id>/cut_mechanic/<mechanic_id>', methods=['DELETE'])
def cut_mechanic (service_id, mechanic_id):
   
    service = db.session.get(ServiceTickets, service_id)  
    mechanic = db.session.get(Inventory, mechanic_id) 
    
    if mechanic not in service.mechanics:
        return jsonify({"message": "Invalid mechanic id"}), 400

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"succefully deleted mechanic {mechanic_id} from {service_id}"}), 200


#==================ADD  inventory to service===================

@serviceTickets_bp.route('/<int:service_id>/add_inventory/<int:inventory_id>', methods=['PUT'])
def add_inventory(service_id, inventory_id):
    service = db.session.get(ServiceTickets, service_id) #can use .get when querying using Primary Key
    inventory = db.session.get(Inventory, inventory_id)

    if service and inventory: #check to see if both exist
        if inventory not in service.inventories: 
            service.inventories.append(inventory) 
            db.session.commit() 
            return jsonify({"Message": "Successfully added inventory to service."}), 200
        else:
            return jsonify({"Message": "inventory is already included in this service."}), 400
    else:
        return jsonify({"Message": "Invalid service id or inventory id."}), 400
 #============Get all services for a customer========================
 
""" @serviceTickets_bp.route("/service/customers/<customer_id>",methods=['GET']) 

def get_customer_service(customer_id): 
    print("id",customer_id)
    customer=db.session.get(Customer,customer_id) 
    print("customer",customer)
    return service_schema.jsonify(customer.service), 200 """

""" #==============Get all mechanics for an service=================

@serviceTickets_bp.route('/service/<int:service_id>/mechanics', methods=['GET'])
def get_service_mechanic(service_id):
    service = db.session.get(ServiceTickets, service_id)
    return mechanics_schema.jsonify(service.mechanics), 200  """
    
    