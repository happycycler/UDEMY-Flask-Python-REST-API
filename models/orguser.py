from db import db

class OrgUserModel(db.Model):
    __tablename__ = 'orgs_users'

    orgid = db.Column(db.Integer, db.ForeignKey('orgs.id'), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self, desc):
        self.orgid = orgid,
        self.userid = userid

    def json(self):
        return {"orgid": self.orgid,
                "org": self.org.name,
                "userid": self.userid,
                "user": self.user.firstname + ' ' + self.user.lastname}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_orgid(cls, orgid):
        return cls.query.filter_by(orgid=orgid).all()

    @classmethod
    def find_by_userid(cls, userid):
        return cls.query.filter_by(userid=userid).all()