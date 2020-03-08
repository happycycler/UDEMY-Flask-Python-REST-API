from db import db
from datetime import datetime

class CourseModel(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    orgid = db.Column(db.Integer, db.ForeignKey('orgs.id'))
    name = db.Column(db.String(255))
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)
    classdate = db.Column(db.Date)
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    classdays = db.Column(db.Text)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))

    course = db.relationship('SubrequestModel', backref='course', lazy='dynamic',
                                foreign_keys='SubrequestModel.classid')

    def __init__(self, orgid, name, starttime, endtime, classdate, startdate, enddate, classdays, userid):
        self.orgid = orgid
        self.name = name
        self.starttime = starttime
        self.endtime = endtime
        self.classdate = classdate
        self.startdate = startdate
        self.enddate = enddate
        self.classdays = classdays
        self.userid = userid

    def json(self):
        return {"id": self.id,
                "orgid": self.orgid,
                "org": self.org.name,
                "name": self.name,
                "starttime": self.starttime.strftime("%I:%M %p"),
                "endtime": self.endtime.strftime("%I:%M %p"),
                "classdate": self.classdate.__str__(),
                "startdate": self.startdate.__str__(),
                "enddate": self.enddate.__str__(),
                "classdays": self.classdays,
                "userid": self.userid,
                "instructor": self.instructor.firstname + " " + self.instructor.lastname}


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
    def find_by_userid(cls, userid):
        return cls.query.filter_by(userid=userid).all()