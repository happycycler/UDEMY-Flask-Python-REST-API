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
    cellcarrierid = db.Column(db.Integer)
    cellphone = db.Column(db.String(25))
    sendtextfl = db.Column(db.Integer)

    def __init__(self, firstname, lastname, username, email, password, validationcode, active, sendemailfl, cellcarrierid, cellphone, sendtextfl):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.validationcode = validationcode
        self.active = active
        self.sendemailfl = sendemailfl
        self.cellcarrierid = cellcarrierid
        self.cellphone = cellphone
        self.sendtextfl = sendtextfl

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
                "cellcarrierid": self.cellcarrierid,
                "cellphone": self.cellphone,
                "sendtextfl": self.sendtextfl}

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
        return cls.query.filter_by(id=_id).first()