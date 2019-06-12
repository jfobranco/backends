from app import db
from flask_restplus import Namespace, Resource, fields
from app.models import Session, User, Service, SessionSchema
from flask import jsonify, request
from .dto import sessionDTO, serviceDTO
import datetime

api = Namespace('sessions', description='Sessions api')

session_schema = SessionSchema()
session_schema_list = SessionSchema(many=True)

@api.route('/')
class SessionListResource(Resource):
    def get(self):
        ''' Get current user sessions? '''
        sessions = Session.query.filter(User.id == 1).options(db.joinedload('services')).all()
        print(sessions[0].services)
        return session_schema_list.jsonify(sessions)

    @api.marshal_with(sessionDTO, code=201)
    @api.expect(sessionDTO)
    def post(self):
        session = Session(status='Started', startDate=datetime.datetime.now(), company_id=api.payload['companyId'], user_id=api.payload['userId'])
        db.session.add(session)
        db.session.commit()
        return session_schema.jsonify(session)

@api.route('/<int:id>')
class SessionResource(Resource):
    def get(self, id):
        session = Session.query.get_or_404(id)
        return session

@api.route('/<int:sessionId>/services/<int:serviceId>')
class SessionServiceResource(Resource):
    def post(self, sessionId, serviceId):
        session = Session.query.get_or_404(sessionId)
        service = Service.query.get_or_404(serviceId)
        session.services.append(service)
        db.session.commit()