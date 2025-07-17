import jwt
from datetime import datetime,timezone,timedelta
from functools import wraps
from flask import request,jsonify
from app.models import Customer
from app.models import db
import os


SECRET_KEY = os.environ.get('SECRET_KEY') or "super secret secrets"

def encode_token(customer_id):
    custStr = str(customer_id)
    payload = {
        'exp' : datetime.now(timezone.utc)+timedelta(hours=1),
        'iat' : datetime.now(timezone.utc),
        'sub' : custStr 
    }
    
    token = jwt.encode(payload,SECRET_KEY,algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
        
        if 'Authorization' in request.headers:
            token=request.headers['Authorization'].split()[1]
            if not token:
                return jsonify({'message':'missing token'}),400
            
            try:
                data=jwt.decode(jwt=token,key=SECRET_KEY,algorithms='HS256')
                customer_id = data['sub']
                customer= db.session.get(Customer,customer_id)
                if not customer:
                    return jsonify({"message":"invalid token because customer doesnt exist"})
                
            except jwt.ExpiredSignatureError as e:
                return jsonify({'message':'token expired'}),400
            except jwt.InvalidTokenError as e:
                return jsonify({'message':'invalid token'}),400
            return f(customer_id , *args, **kwargs)
        else:
            return jsonify({'message':'you must be logged in to access this.'}),400
        
    return decorated
            