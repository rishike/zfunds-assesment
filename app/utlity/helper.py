import random
import string
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
from functools import wraps

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def generate_unique_product_link(purchase_id):
    return f'{request.url_root}api/product/{purchase_id}'


def generate_token(mobile_number):
    
    admin = {
        'mobile_number': mobile_number,
        'role': 'admin'
    }

    access_token = create_access_token(identity=admin)
    return access_token


def custom_jwt_required(fn):
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            current_claims = get_jwt_identity()
            
            if 'admin' in current_claims.get('roles', []):
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized"})
        except NoAuthorizationError:
            return jsonify({"message": "Authorization header is missing"})
        except JWTExtendedException as e:
            return {}

    return wrapper
