#/usr/bin/python3
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import  BadSignature, SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer
from sqlalchemy import Column, Integer, String, Float, Unicode
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from datetime import  datetime

from passlib.apps import custom_app_context as pwd_context

secret_key = 'secretkey1234'

Base = declarative_base()

db = SQLAlchemy(model_class=Base)

class Product(Base):
    __tablename__ ='products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(EncryptedType(Unicode,
                                           secret_key,
                                           AesEngine,
                                           'pkcs5'), unique=True,index=True, nullable=False)
    description= Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    username = Column(String(32), index = True)
    password = Column(EncryptedType(Unicode,
                                           secret_key,
                                           AesEngine,
                                           'pkcs5'))

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
    def generate_auth_token(self, expiration = 600):
        s = Serializer(secret_key)
        return s.dumps({'id': self.id, 'timestamps' : datetime.now().strftime("%s")})
    

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
            print(data)
        except SignatureExpired:
            print("Valid token error")
            return None # valid token, but expired
        except BadSignature:
            print("Invalide token")
            return None # invalid token
        if (int(datetime.now().strftime("%s")) - int(data['timestamps'])  > 720 ):
            print("Token trop ancien")
            return None
        user = User.query.get(data['id'])
        #print(user)
        return user
    
    def get_auth_token(self):
        token = self.generate_auth_token()
        print("Token %s" % token )
        return token