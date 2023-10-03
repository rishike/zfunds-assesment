from flask_restful import Resource, reqparse
from app.models.User import User
from database import db
from flask import request
from flask import current_app as app


class AddClient(Resource):
    
    def post(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('advisor_number', type=str, required=True)
        parser.add_argument('client_name', type=str, required=True)
        parser.add_argument('client_number', type=str, required=True)
        args = parser.parse_args()
        
        client_number = args['client_number']

        # Check if the advisor exists
        advisor = User.query.filter_by(mobile_number=args['advisor_number'], role='advisor').first()
        existing_client = User.query.filter_by(mobile_number=client_number).first()
        
        if existing_client:
            return {'message': 'Client with the same mobile number already exists.'}, 400
        
        if not advisor:
            return {'message': 'Advisor not found.'}, 404

        # Create a new client user with role user
        new_client = User(name=args['client_name'] , mobile_number=client_number, role='user', advisor_id=advisor.id)
        db.session.add(new_client)
        db.session.commit()

        return {
            'message': 'Client added successfully',
            'client_name': args['client_name'],
            'client_mobile_number': args['client_number'],
            'advisor_mobile_number': args['advisor_number']
        }, 201


class ViewClient(Resource):
    
    def get(self, advisor_id):
        advisor = User.query.filter_by(role='advisor', id=advisor_id).first()

        if not advisor:
            return {'message': 'Advisor not found.'}, 404

        if advisor.role != 'advisor':
            return {'message': 'Invalid advisor ID.'}, 400

        clients = User.query.filter_by(role='user').filter_by(advisor_id=advisor.id).all()
        print(clients)
        client_list = [{'id': client.id, 'name' : client.name ,'mobile_number': client.mobile_number} for client in clients]

        return {
            'message': 'List of clients for advisor',
            'clients': client_list
        }, 200


