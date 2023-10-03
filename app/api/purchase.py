from flask_restful import Resource, reqparse
from app.models.Product import Product
from app.models.User import User
from app.models.Purchase import Purchase
from database import db
from app.utlity.helper import generate_unique_product_link
from flask import current_app as app


class PurchaseProductApi(Resource):
    def post(self):
        
        app.logger.info("calling PurchaseProductApi")
        parser = reqparse.RequestParser()
        parser.add_argument('advisor_mobile_number', type=str, required=True)
        parser.add_argument('client_mobile_number', type=str, required=True)
        parser.add_argument('product_id', type=int, required=True)
        args = parser.parse_args()

        # Check if the advisor and client exist
        advisor = User.query.filter_by(mobile_number=args['advisor_mobile_number'], role='advisor').first()
        client = User.query.filter_by(mobile_number=args['client_mobile_number'], role='user', advisor_id=advisor.id).first()

        if not advisor or not client:
            return {'message': 'Advisor or client not found.'}, 404
        

        # Check if the product exists
        product = Product.query.get(args['product_id'])
        if not product:
            return {'message': 'Product not found.'}, 404

        # Create a new purchase
        new_purchase = Purchase(
            advisor_id=advisor.id,
            user_id=client.id,
            product_id=product.id
        )
        db.session.add(new_purchase)
        db.session.commit()
        
        app.logger.info("Successfully purchase product")

        product_link = generate_unique_product_link(new_purchase.id)
        
        app.logger.info(f"Successfully generated product link : {product_link}")

        return {
            'message': 'Product purchased successfully',
            'product_link': product_link
        }, 201


