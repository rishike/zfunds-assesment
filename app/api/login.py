from flask_restful import Resource, reqparse
from app.utlity.helper import generate_token
from app.models.User import User


class Login(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mobile_number', type=str, required=True)
        args = parser.parse_args()
        
        mobile = args['mobile_number']
        
        admin_user = User.query.filter_by(mobile_number=mobile, role='admin').first()
        
        if not admin_user:
            return {'message': 'Not a admin.'}, 403
        
        access_token = generate_token(mobile)
        return {'access_token': access_token}, 200