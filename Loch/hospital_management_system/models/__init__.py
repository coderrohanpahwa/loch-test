from hospital_management_system import db
from datetime import datetime
class ParentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())    
    __abstract__ = True
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.get(id)
    
    def to_json(self):
        return {col.name: str(getattr(self, col.name)) for col in self.__table__.columns}        

    @classmethod
    def find_by(cls,field,value):
        return cls.query.filter_by(**{field:value}).all()
    @classmethod
    def find_all(cls):
        return cls.query.all()