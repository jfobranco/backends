from app import db
from flask_restplus import Namespace, Resource, fields
from app.models import User, UserSchema, Post, Company, PostSchema
from flask import jsonify, request
from .dto import userDTO, postDTO

api = Namespace('users', description='Users api')

user_schema = UserSchema()
user_schema_list = UserSchema(many=True)

post_schema = PostSchema()
post_schema_list = PostSchema(many=True)

@api.route('/')
class UsersResourceList(Resource):
    @api.marshal_with(userDTO, code=201)
    @api.expect(userDTO)
    def post(self):
        users = User.query.all()
        return user_schema_list.jsonify(users)

@api.route('/<int:id>')
class UsersResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user_schema.jsonify(user)

@api.route('/<int:id>/posts')
class UsersResourcePosts(Resource):
    def get(self, id):
        ''' Get user feed  '''
        query = db.session.query(Post).filter(Post.company_id == Company.id).filter(Company.followers.any()).filter(User.id == id)
        posts = query.all()
        return post_schema_list.jsonify(posts)