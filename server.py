from flask import Flask
import logging
from flask_restful import Api
from app.models.User import User
from app.api.signup import RequestOtpApi,AdvisorSignupApi,UserSignupApi
from app.api.client import AddClientApi, ViewClientApi
from app.api.product import AddProductApi, GetProductDetailsApi
from app.api.purchase import PurchaseProductApi
from app.api.login import LoginApi
from database import db
from datetime import datetime
from flask_jwt_extended import JWTManager


# logging.basicConfig(
#           filename=f"logs/log_{datetime.strftime(datetime.now(), '%Y_%m_%d')}.log",
#           filemode='a',
#           format='%(asctime)s %(levelname)s %(message)s',
#           datefmt='%H:%M:%S',
#           level=logging.DEBUG)



app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

api = Api(app, prefix="/api")
api.add_resource(RequestOtpApi, '/generate-otp')
api.add_resource(AdvisorSignupApi, '/advisor/signup')
api.add_resource(AddClientApi, '/advisor/add_client')
api.add_resource(ViewClientApi, '/advisor/view_clients/<int:advisor_id>')
api.add_resource(UserSignupApi, '/user/signup')
api.add_resource(LoginApi, '/admin/login')
api.add_resource(AddProductApi, '/admin/add_product')
api.add_resource(PurchaseProductApi, '/advisor/purchase_product')
api.add_resource(GetProductDetailsApi, '/product/<int:purchase_id>')





db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # Only for debugging while developing
    app.run(debug=True)