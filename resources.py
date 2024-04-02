from sqlalchemy.exc import IntegrityError
from flask import app, jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from models import Product, User, db
from schema import ProductSchema, UserSchema


class ProductResource(Resource):

    product_schema = ProductSchema()
    product_list_schema = ProductSchema(many=True)
    product_patch_schema = ProductSchema(partial=True) 

    def get(self,product_id=None):

        if product_id:
            product = Product.query.get_or_404(product_id)
            return self.product_schema.dump(product)
        else:
            all_products = Product.query.all()
            return self.product_list_schema.dump(all_products)

    def post(self):
        if not User.verify_auth_token(request.headers['Authorization']):
            return jsonify(msg="Invalid token")
        try:
            new_product_data = self.product_schema.load(request.json)
        except ValidationError as err:
            return {"message":"Validation Error", "errors": err.messages}, 400

        new_product = Product(
            name = new_product_data['name'],
            description = new_product_data['description'],
            price = new_product_data['price']
        )

        try: 
            db.session.add(new_product)
            db.session.commit()
        except IntegrityError as err:
            return {"message":"Constraint error", "errors": err.detail}, 400

        return self.product_schema.dump(new_product)

    def put(self, product_id):
        try:
            new_product_data = self.product_schema.load(request.json)
        except ValidationError as err:
            return {"message":"Validation Error", "errors": err.messages}, 400

        product = Product.query.get_or_404(product_id)
        for key , value in new_product_data.items():
            setattr(product,key,value)

        db.session.commit()
        return self.product_schema.dump(product)

    def patch(self, product_id):
        try:
            new_product_data = self.product_patch_schema.load(request.json)
        except ValidationError as err:
            return {"message":"Validation Error", "errors": err.messages}, 400

        product = Product.query.get_or_404(product_id)
        for key , value in new_product_data.items():
            setattr(product,key,value)

        db.session.commit()
        return self.product_schema.dump(product)

    def delete(self,product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class UserResource(Resource):
    user_schema = UserSchema()
    def post(self):
        try:
            print("User.Post")
            print(request.json)
            new_user_data = self.user_schema.load(request.json)
            
        except ValidationError as err:
            return {"message":"Validation Error", "errors": err.messages}, 400

        new_user = User(
            username = new_user_data['username'],
            password = new_user_data['password']
            #user.hash_password(password)
        )
        print("Persist")
        db.session.add(new_user)
        db.session.commit()
        token=new_user.get_auth_token()
        #User.verify_auth_token(token)

        return jsonify(token=token)
