from dotenv import load_dotenv

loaded = load_dotenv()

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .blueprints.operations import operations_blueprint
from .errors.errors import ApiError
from .extensions import db
import os


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
)

app.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager(app)

# Inicializa SQLAlchemy con la aplicación Flask
db.init_app(app)

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()

app.register_blueprint(operations_blueprint)


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {"msg": err.description}
    return jsonify(response), err.code
