from db import db
from datetime import datetime

class CarrierModel(db.Model):
    __tablename__ = 'carriers'

    id = db.Column(db.Integer, primary_key=True)
    carriername = db.Column(db.String(25))
    carrierdomain = db.Column(db.String(25))

    users = db.relationship('UserModel', lazy='dynamic')

    def __init__(self, carriername, carrierdomain):
        self.carriername = carriername
        self.carrierdomain = carrierdomain

    def json(self):
        return {"id": self.id,
                "carriername": self.carriername,
                "carrierdomain": self.carrierdomain}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(carriername=name).first()