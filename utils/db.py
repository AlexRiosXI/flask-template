from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime

db = SQLAlchemy()

    

def parse_query(model_instance,fields=[]):
    json = {}
    for attribute, value in model_instance.__dict__.items():
        if re.search("_sa_instance_state",attribute):
            pass
        else:
            json[str(attribute)] = value
    if len(fields) == 0:
        pass
    else:
        temp_json = {}
        for field in fields:
            temp_json[field] = json[field]
        json = temp_json
    return json

class Model(db.Model):
    __abstract__ = True

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()

    def commit(self):
        db.session.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            db.session.commit()
    def to_dict(self, fields=[]):
        return parse_query(self, fields)

class ModelTimeStamp(Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    def update(self, commit=True):
        self.updated_at = datetime.utcnow()
        super().commit()

    
class ModelTimeStampSoftDelete(ModelTimeStamp):
    __abstract__ = True
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self, commit=True):
        self.deleted_at = datetime.utcnow()
        super().commit()

    def restore(self, commit=True):
        self.deleted_at = None
        super().commit()




        

        
        
        
        