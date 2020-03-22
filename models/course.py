from db import db
from datetime import datetime
from platform import system
from models.subrequest import SubrequestModel

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
    requestuserid = db.Column(db.Integer, db.ForeignKey('users.id'))
    requestdate = db.Column(db.Date)
    acceptuserid = db.Column(db.Integer, db.ForeignKey('users.id'))
    acceptdate = db.Column(db.Date)

    def __init__(self, orgid, name, starttime, endtime, classdate, startdate, enddate, classdays, userid, requestuserid, requestdate, acceptuserid, acceptdate):
        self.orgid = orgid
        self.name = name
        self.starttime = starttime
        self.endtime = endtime
        self.classdate = classdate
        self.startdate = startdate
        self.enddate = enddate
        self.classdays = classdays
        self.userid = userid
        self.requestuserid = requestuserid
        self.requestdate = requestdate
        self.acceptuserid = acceptuserid
        self.acceptdate = acceptdate

    def json(self):
        subrequeststatus = None
        if self.requestuserid != None and self.acceptuserid != None:
            subrequeststatus = 'accepted'

        if self.requestuserid != None and self.acceptuserid == None:
            subrequeststatus = 'requested'

        return {"id": self.id,
                "orgid": self.orgid,
                "orgname": self.org.name,
                "name": self.name,
                "starttime": self.starttime.strftime("%#I:%M %p") if system() == 'Windows' else self.starttime.strftime("%-I:%M %p"),
                "endtime": self.endtime.strftime("%#I:%M %p") if system() == 'Windows' else self.endtime.strftime("%-I:%M %p"),
                "classdate": self.classdate.strftime("%m/%d/%Y"),
                "startdate": self.startdate.strftime("%m/%d/%Y"),
                "enddate": self.enddate.strftime("%m/%d/%Y"),
                "classdays": self.classdays,
                "userid": self.userid,
                "instructor": self.instructor.firstname + " " + self.instructor.lastname,
                "classid": self.id,
                "originstructor": self.instructor.firstname + " " + self.instructor.lastname,
                "requestuserid": self.requestuserid,
                "requestuser": self.requestuser.firstname + " " + self.requestuser.lastname if self.requestuserid != None else None,
                "requestdate": self.requestdate.strftime("%m/%d/%Y") if self.requestuserid != None else None,
                "acceptuserid": self.acceptuserid,
                "acceptinstructor": self.acceptuser.firstname + " " + self.acceptuser.lastname if self.acceptuserid != None else None,
                "acceptdate": self.acceptdate.strftime("%m/%d/%Y") if self.acceptuserid != None else None,
                "subrequeststatus": subrequeststatus}

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
    def find_by_userid(cls, uid, allrequests):
        if allrequests == 'true':
            return cls.query.filter(cls.classdate >= datetime.strftime(datetime.today().date(), '%Y-%m-%d')).filter(cls.requestuserid != None).order_by(cls.classdate, cls.starttime, cls.name).all()
        else:
            # return cls.query.filter(cls.userid == uid).filter(cls.classdate >= datetime.today()).order_by(cls.classdate, cls.starttime, cls.name).all()
            return cls.query.filter(cls.userid == uid).filter(cls.classdate >= datetime.strftime(datetime.today().date(), '%Y-%m-%d')).order_by(cls.classdate, cls.starttime, cls.name).all()