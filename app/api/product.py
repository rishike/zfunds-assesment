from flask_restful import Resource, reqparse
from database import db
from flask import current_app as app
from app.models.Product import Category, Product
from app.models.Purchase import Purchase
from app.models.User import User
from flask_jwt_extended import jwt_required, get_jwt_identity




class AddProductApi(Resource):
    
    @jwt_required()
    def post(self):
        app.logger.info("calling AddProductApi")
        parser = reqparse.RequestParser()
        parser.add_argument('product_name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('category_name', type=str, required=True)
        args = parser.parse_args()
        
        current_user = get_jwt_identity()
        admin_user = User.query.filter_by(mobile_number=current_user.get('mobile_number'), role='admin').first()

        if not admin_user:
            return {'message': 'Only admin can add products.'}, 401

        category_name = args['category_name']
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            app.logger.info(f"created new category {category_name}")

        # Create a new product
        new_product = Product(
            name=args['product_name'],
            description=args['description'],
            category_id=category.id
        )
        db.session.add(new_product)
        db.session.commit()
        app.logger.info("Successfully added product")

        return {
            'message': 'Product added successfully',
            'id': new_product.id,
            'name': new_product.name,
            'category': category.name
        }, 201


class GetProductDetailsApi(Resource):
    def get(self, purchase_id):
        
        app.logger.info("calling GetProductDetailsApi")
        purchase = Purchase.query.get(purchase_id)

        if not purchase:
            return {'message': 'Purchase not found.'}, 404

        advisor_id = purchase.advisor.id
        client_name = purchase.user.name
        product_name = purchase.product.name

        return {
            'advisor_id': advisor_id,
            'client_name': client_name,
            'product_name': product_name
        }, 200