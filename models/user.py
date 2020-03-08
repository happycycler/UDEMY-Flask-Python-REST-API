from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    validationcode = db.Column(db.String(255))
    active = db.Column(db.Integer)
    sendemailfl = db.Column(db.Integer)
    carrierid = db.Column(db.Integer, db.ForeignKey('carriers.id'))
    cellphone = db.Column(db.String(25))
    sendtextfl = db.Column(db.Integer)
    privid = db.Column(db.Integer, db.ForeignKey('privs.id'))

    instructor = db.relationship('CourseModel', backref='instructor', lazy='dynamic',
                                    foreign_keys='CourseModel.userid')
    requester = db.relationship('SubrequestModel', backref='requestuser', lazy='dynamic',
                                    foreign_keys='SubrequestModel.requestuserid')
    acceptor = db.relationship('SubrequestModel', backref='acceptuser', lazy='dynamic',
                                    foreign_keys='SubrequestModel.acceptuserid')
    orguseruser = db.relationship('OrgUserModel', backref='user', lazy='dynamic',
                                    foreign_keys='OrgUserModel.userid')

    def __init__(self, firstname, lastname, username, email, password, validationcode, active, sendemailfl, carrierid, cellphone, sendtextfl, privid):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.validationcode = validationcode
        self.active = active
        self.sendemailfl = sendemailfl
        self.carrierid = carrierid
        self.cellphone = cellphone
        self.sendtextfl = sendtextfl
        self.privid = privid

    def json(self):
        return {"id": self.id,
                "firstname": self.firstname,
                "lastname": self.lastname,
                "username": self.username,
                "email": self.email,
                "password": self.password,
                "validationcode": self.validationcode,
                "active": self.active,
                "sendmailfl": self.sendemailfl,
                "carrierid": self.carrierid,
                "carrier": self.carrier.carriername,
                "cellphone": self.cellphone,
                "sendtextfl": self.sendtextfl,
                "privid": self.privid,
                "priv": self.priv.desc}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).all()