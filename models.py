#/usr/bin/python3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Unicode
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

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
