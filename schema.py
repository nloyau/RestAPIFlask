from flask_marshmallow import Marshmallow
from models import Product, User

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Product()

class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User()