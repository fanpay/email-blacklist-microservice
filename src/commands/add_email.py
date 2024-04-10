import re
import logging


from .base_command import BaseCommannd
from ..errors.errors import EmailBadRequestError, EmailAlreadyExistsError
from ..models.blacklist import BlackList
from ..extensions import db

logging.basicConfig(level=logging.INFO)

class ViewAddEmail(BaseCommannd):
    def __init__(self, data_json, client_ip):
        self.validate_data(data_json)
        self.validate_existing_email(data_json["email"])
        
        self.client_ip = client_ip
        self.data_json = data_json

    def execute(self):
        new_email = BlackList(
            email=self.data_json["email"],
            app_uuid=self.data_json["app_uuid"],
            blocked_reason=self.data_json.get("blocked_reason", None),
            from_ip = self.client_ip
        )

        db.session.add(new_email)
        db.session.commit()

        return new_email

    def validate_data(self, data):
        if not all(key in data for key in ("email", "app_uuid")) or (
            not self.check_email(data["email"])
        ):
            raise EmailBadRequestError   
        
    def check_email(self, texto):
        # Expresión regular para validar direcciones de correo electrónico
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # re.match para verificar si el texto coincide con el patrón
        if re.match(pattern, texto):
            return True
        else:
            return False
        
    def validate_existing_email(self, email):
        existing_email = BlackList.query.filter_by(email=email).first()

        if existing_email:
            raise EmailAlreadyExistsError