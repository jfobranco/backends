from datetime import datetime
from . import db
from . import ma

user_company = db.Table('user_company', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.name)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followers = db.relationship('User', secondary=user_company)
    posts = db.relationship('Post', back_populates="parent")

    def __repr__(self):
        return '<Company {} {}>'.format(self.id, self.name)

class CompanySchema(ma.TableSchema):
    class Meta:
        table = Company.__table__

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    parent = db.relationship("Company", back_populates="posts")

    def __repr__(self):
        return '<Post {}>'.format(self.title)

class PostSchema(ma.TableSchema):
    class Meta:
        table = Post.__table__

session_service = db.Table('session_service', db.Model.metadata,
    db.Column('session_id', db.Integer, db.ForeignKey('session.id')),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'))
)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(140))
    startDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    endDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    services = db.relationship('Service', secondary=session_service)

    def __repr__(self):
        return '<Session {}>'.format(self.status)

class SessionSchema(ma.TableSchema):
    class Meta:
        table = Session.__table__

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    category = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    def __repr__(self):
        return '<Service {}>'.format(self.name)

class ServiceSchema(ma.TableSchema):
    class Meta:
        table = Service.__table__