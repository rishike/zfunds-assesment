from flask_restful import Resource, reqparse
from app.models.User import User, OTP
from app.utlity.helper import generate_otp
from database import db
import jwt
from flask import current_app as app

class RequestOtpApi(Resource):
    
    
    def post(self):
        
        app.logger.info("calling RequestOtpApi")
        parser = reqparse.RequestParser()
        parser.add_argument('mobile_number', type=str, required=True)
        args = parser.parse_args()
        
        app.logger.info(f"{args} requested data")
    
        mobile =  args['mobile_number']
        
        # Generate and store a new OTP in database
        otp = generate_otp()
        exist_otp = OTP.query.filter_by(mobile_number=mobile).first()
        if exist_otp:
            exist_otp.otp = otp
            app.logger.info(f"otp already exists. Updating with new otp.")
        else:
            otp_entry = OTP(mobile_number=mobile, otp=otp)
            db.session.add(otp_entry)
            
        db.session.commit()
        app.logger.info("Successfully send and generate otp")
        
        return {'message': 'OTP sent successfully.', 'OTP': otp}

class AdvisorSignupApi(Resource):
  
    def post(self):
        
        app.logger.info("calling AdvisorSignupApi")
        parser = reqparse.RequestParser()
        parser.add_argument('mobile_number', type=str, required=True)
        parser.add_argument('otp', type=int, required=True)
        args = parser.parse_args()
        
        app.logger.info(f"{args} requested data")
    
    
        mobile =  args['mobile_number']
        user_otp = args['otp']
        
        otp_obj = OTP.query.filter_by(mobile_number=mobile).first()

        if not otp_obj or otp_obj.otp != int(user_otp):
            return {'msg': "otp error. Please generate new otp"}, 403
        
        
        jwt_secret_key = app.config['SECRET_KEY']
        # Check if the mobile number already exists
        existing_user = User.query.filter_by(mobile_number=mobile, role='advisor').first()
        if existing_user:
            if existing_user.verified:
                return {'message': 'Mobile number with this Advisor already exists.'}, 400
            else:
                existing_user.verified = True
            payload = {'user_id': existing_user.id, 'role': existing_user.role}
        else:
            # Create a new advisor account
            new_advisor = User(mobile_number=mobile, role='advisor', verified=True)
            db.session.add(new_advisor)
            payload = {'user_id': new_advisor.id, 'role': new_advisor.role}
        db.session.commit()
        app.logger.info("advisor created successfully")
        
        token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
        app.logger.info(f"{token} generated.")

        return {'message': 'Advisor account created successfully', 'token': token}, 201

class UserSignupApi(Resource):
    
    def post(self):
        app.logger.info("calling UserSignupApi")
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('mobile_number', type=str, required=True)
        parser.add_argument('otp', type=int, required=True)
        args = parser.parse_args()
        
        mobile = args['mobile_number']
        user_otp = args['otp']
        name = args['name']

        # Check if the mobile number already exists
        existing_user = User.query.filter_by(mobile_number=mobile).first()
        if existing_user:
            return {'message': 'Mobile number already exists.'}, 400

        
        exist_otp = OTP.query.filter_by(mobile_number=mobile).first()
        
        if not exist_otp or user_otp != exist_otp.otp:
            return {'message': 'Invalid OTP.'}, 400

        # Create a new user account with role 'user'
        new_user = User(name=name, mobile_number=mobile, role='user', verified=True)
        db.session.add(new_user)
        db.session.commit()
        
        app.logger.info("Successfully created User")
        
        return {
            'message': 'User account created successfully',
            'name': name,
            'mobile_number': name
        }, 201

