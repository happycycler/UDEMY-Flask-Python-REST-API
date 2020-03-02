from db import db
from datetime import datetime

class OrgModel(db.Model):
    __tablename__ = 'orgs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(25))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(5))
    phone = db.Column(db.String(12))
    status = db.Column(db.String(10))

    courses = db.relationship('CourseModel', lazy='dynamic')

    def __init__(self, name, address1, address2, city, state, zip, phone, status):
        self.name = name
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip = zip
        self.phone = phone
        self.status = status

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "state": self.state,
                "zip": self.zip,
                "phone": self.phone,
                "status": self.status}

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
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).all()