from db import db
from datetime import datetime

class PrivModel(db.Model):
    __tablename__ = 'privs'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(25))

    userpriv = db.relationship('UserModel', backref='priv', lazy='dynamic',
                                 foreign_keys='UserModel.privid')

    def __init__(self, desc):
        self.desc = desc

    def json(self):
        return {"id": self.id,
                "desc": self.desc}

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
        return cls.query.filter_by(desc=name).first()