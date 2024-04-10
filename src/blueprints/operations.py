from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required

from ..commands.add_email import ViewAddEmail
from ..commands.check_email import ViewCheckEmail
from ..commands.ping import ViewPing
from ..commands.create_token import ViewGenerateToken
from ..commands.blacklist_reset import ViewBlackListReset

operations_blueprint = Blueprint("operations", __name__)


@operations_blueprint.route("/blacklists/ping", methods=["GET"])
def ping():
    return ViewPing().execute()


@operations_blueprint.route("/blacklists", methods=["POST"])
@jwt_required()
def add_email_to_blacklist():
    data = request.get_json()
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"La solicitud fue realizada desde la dirección IP: {client_ip}", flush=True)
    result = ViewAddEmail(data, client_ip).execute()
    response_data = {
        "message": f"Email {result.email} fue agregado exitosamente.",
        "createdAt": result.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    return jsonify(response_data), 200


@operations_blueprint.route("/blacklists/<string:email>", methods=["GET"])
@jwt_required()
def check_email_blacklist(email):
    response = ViewCheckEmail(email=email).execute()

    return jsonify(response), 200


@operations_blueprint.route("/blacklists/auth", methods=["GET"])
def create_token():
    generated_access_token = ViewGenerateToken().execute()

    response_data = {
        "token": generated_access_token
    }

    return jsonify(response_data), 200



@operations_blueprint.route("/blacklists/reset", methods=["POST"])
@jwt_required()
def reset():
    ViewBlackListReset().execute()

    response_data = {"msg": "Todos los datos fueron eliminados"}

    return jsonify(response_data), 200
