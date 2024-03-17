import bcrypt
from . import ParentModel
from hospital_management_system import db

from datetime import datetime
class UsersModel(ParentModel):
    __tablename__ = 'users'
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    access_token = db.Column(db.Text)
    last_login = db.Column(db.DateTime)


    @staticmethod
    def generate_password_hash(password):
        return str(bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10)).decode('utf8'))
        

    @staticmethod
    def verify_hash(password, hashed):
        return bcrypt.checkpw(password.encode('utf8'), hashed.encode('utf8'))

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()