from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restplus import Api

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

from app.api import api
api.init_app(app)

from app import routes