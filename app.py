from flask import Flask, abort, jsonify, request, url_for
from flask_restful import Api
from models import Product, User, db
from resources import ProductResource, UserResource
from schema import ma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

db.init_app(app)
ma.init_app(app)

api = Api(app)

api.add_resource(UserResource, '/api/users')
api.add_resource(ProductResource, '/products','/product/<int:product_id>')



with app.app_context():
    try:
        #db.drop_all()
        #db.create_all()

        #test = Product(name="Test",description="desc",price="20")

        #db.session.add(test)
        #db.session.commit()

        mon_test = db.session.query(Product).filter(Product.name == "Test").first()
        print(f"{mon_test.id} {mon_test.name}: {mon_test.description}")

    except(e):
        print("erreur")
