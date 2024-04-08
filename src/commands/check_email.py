import re
import logging


from .base_command import BaseCommannd
from ..errors.errors import EmailBadRequestError, EmailAlreadyExistsError
from ..models.blacklist import BlackList
from ..extensions import db

logging.basicConfig(level=logging.INFO)

class ViewCheckEmail(BaseCommannd):
    def __init__(self, email):
        self.validate_email_format(email)
        self.email = email

    def execute(self):
        return self.get_existing_email(self.email)

    def validate_data(self, data):
        if not all(key in data for key in ("email", "app_uuid")) or (
            not self.check_email(data["email"])
        ):
            raise EmailBadRequestError   
        
    def validate_email_format(self, texto):
        # Expresión regular para validar direcciones de correo electrónico
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        # re.match para verificar si el texto coincide con el patrón
        if re.match(pattern, texto):
            return True
        else:
            return False
        
    def get_existing_email(self, email):
        existing_email = BlackList.query.filter_by(email=email).first()

        if existing_email:
            return {
                "email_exists": True,
                "blocked_reason": existing_email.blocked_reason
            }
        else:
            return {
                "email_exists": False,
                "blocked_reason":""
            }
        
