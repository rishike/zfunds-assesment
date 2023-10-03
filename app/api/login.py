from flask_restful import Resource, reqparse
from app.utlity.helper import generate_token
from app.models.User import User
from flask import current_app as app

class LoginApi(Resource):
    
    def post(self):
        
        app.logger.info("calling LoginApi")
        parser = reqparse.RequestParser()
        parser.add_argument('mobile_number', type=str, required=True)
        args = parser.parse_args()
        
        mobile = args['mobile_number']
        
        admin_user = User.query.filter_by(mobile_number=mobile, role='admin').first()
        
        if not admin_user:
            return {'message': 'Not a admin.'}, 403
        
        access_token = generate_token(mobile)
        app.logger.info(f"successfully generated token {access_token}")
        return {'access_token': access_token}, 200