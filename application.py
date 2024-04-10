from dotenv import load_dotenv

loaded = load_dotenv()

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from src.blueprints.operations import operations_blueprint
from src.errors.errors import ApiError
from src.extensions import db
import os


application = Flask(__name__)

if 'RDS_HOSTNAME' in os.environ:
    application.config["SQLALCHEMY_DATABASE_URI"] = (
        f'postgresql://{os.environ["RDS_USERNAME"]}:{os.environ["RDS_PASSWORD"]}@{os.environ["RDS_HOSTNAME"]}:{os.environ["RDS_PORT"]}/{os.environ["RDS_DB_NAME"]}'
    )
else:
    application.config["SQLALCHEMY_DATABASE_URI"] = (
        f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    )
    

application.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]
application.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager(application)

# Inicializa SQLAlchemy con la aplicación Flask
db.init_app(application)

# Crear las tablas de la base de datos
with application.app_context():
    db.create_all()

application.register_blueprint(operations_blueprint)


@application.errorhandler(ApiError)
def handle_exception(err):
    response = {"msg": err.description}
    return jsonify(response), err.code
