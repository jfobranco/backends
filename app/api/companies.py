from app import db
from flask_restplus import Namespace, Resource, fields
from app.models import Company, CompanySchema, User, Post, Service, ServiceSchema
from flask import jsonify, request
from .dto import companyDTO, postDTO, serviceDTO

api = Namespace('companies', description='Companies api')

#currentUser = User.query.get_or_404(1)

#currentUser = User(id=1, name='Test', email='test')
#db.session.add(currentUser)
#db.session.commit()

company_schema = CompanySchema()
company_schema_list = CompanySchema(many=True)

service_schema = ServiceSchema()
service_schema_list = ServiceSchema(many=True)

@api.route('/')
class CompaniesListResource(Resource):
    def get(self):
        comps = Company.query.all()
        return company_schema_list.jsonify(comps)

    @api.marshal_with(companyDTO, code=201)
    @api.expect(companyDTO)
    def post(self):
        comp = Company(name=api.payload['name'], owner_id=1)
        db.session.add(comp)
        db.session.commit()
        return api.payload

@api.route('/<int:id>')
class CompaniesResource(Resource):
    def get(self, id):
        comp = Company.query.get_or_404(id)
        return company_schema.jsonify(comp)

@api.route('/<int:id>/posts')
class CompaniesPostsResource(Resource):
    @api.marshal_with(postDTO, code=201)
    @api.expect(postDTO)
    def post(self, id):
        post = Post(title=api.payload['title'], content=api.payload['content'], company_id=id)
        db.session.add(post)
        db.session.commit()
        return api.payload

@api.route('/<int:id>/users')
class CompaniesFollowResource(Resource):
    def post(self, id):
        ''' Follow company '''
        comp = Company.query.get_or_404(id)
        user = User.query.get_or_404(1)
        comp.followers.append(user)
        db.session.commit()
        return 200

@api.route('/<int:id>/services/')
class CompaniesServices(Resource):
    @api.marshal_with(serviceDTO, code=201)
    @api.expect(serviceDTO)
    def post(self, id):
        service = Service(name=api.payload['name'], category=api.payload['category'], company_id=id)
        db.session.add(service)
        db.session.commit()
        return api.payload
    
    def get(self, id):
        services = Service.query.filter(Company.id == id).all()
        return service_schema_list.jsonify(services)