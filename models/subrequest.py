from db import db
from datetime import datetime

class SubrequestModel(db.Model):
    __tablename__ = 'subrequests'

    id = db.Column(db.Integer, primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey('classes.id'))
    requestuserid = db.Column(db.Integer, db.ForeignKey('users.id'))
    acceptuserid = db.Column(db.Integer, db.ForeignKey('users.id'))
    requestdate = db.Column(db.String)
    acceptdate = db.Column(db.String)

    def __init__(self, classid, requestuserid, acceptuserid, requestdate, acceptdate):
        self.classid = classid
        self.requestuserid = requestuserid
        self.acceptuserid = acceptuserid
        self.requestdate = requestdate
        self.acceptdate = acceptdate

    def json(self):
        if self.acceptuserid == None:
            acceptusername = None
        else:
            acceptusername = self.acceptuser.firstname + ' ' + self.acceptuser.lastname

        return {"id": self.id,
                "classid": self.classid,
                "classname": self.course.name,
                "requestuserid": self.requestuserid,
                "requestuser": self.requestuser.firstname + ' ' + self.requestuser.lastname,
                "acceptuserid": self.acceptuserid,
                "acceptuser": acceptusername,
                "requestdate": self.requestdate.__str__(),
                "acceptdate": self.acceptdate.__str__()}

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
    def find_by_classid(cls, classid):
        return cls.query.filter_by(classid=classid).all()

    @classmethod
    def find_by_requestuserid(cls, requestuserid):
        return cls.query.filter_by(requestuserid=requestuserid).all()

    @classmethod
    def find_by_acceptuserid(cls, acceptuserid):
        return cls.query.filter_by(acceptuserid=acceptuserid).all()