from flask import Flask
import logging
from flask_restful import Api
from app.models.User import User
from app.api.signup import RequestOtp,AdvisorSignup,UserSignup
from app.api.client import AddClient, ViewClient
from app.api.product import AddProduct, GetProductDetails
from app.api.purchase import PurchaseProduct
from app.api.login import Login
from database import db
from datetime import datetime
from flask_jwt_extended import JWTManager


logging.basicConfig(
          filename=f"logs/log_{datetime.strftime(datetime.now(), '%Y_%m_%d')}.log",
          filemode='a',
          format='%(asctime)s %(levelname)s %(message)s',
          datefmt='%H:%M:%S',
          level=logging.DEBUG)



app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

api = Api(app, prefix="/api")
api.add_resource(RequestOtp, '/generate-otp')
api.add_resource(AdvisorSignup, '/advisor/signup')
api.add_resource(AddClient, '/advisor/add_client')
api.add_resource(ViewClient, '/advisor/view_clients/<int:advisor_id>')
api.add_resource(UserSignup, '/user/signup')
api.add_resource(Login, '/admin/login')
api.add_resource(AddProduct, '/admin/add_product')
api.add_resource(PurchaseProduct, '/advisor/purchase_product')
api.add_resource(GetProductDetails, '/product/<int:purchase_id>')





db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(debug=True)