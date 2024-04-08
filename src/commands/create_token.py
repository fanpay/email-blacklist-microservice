import os

from flask_jwt_extended import create_access_token
from .base_command import BaseCommannd


class ViewGenerateToken(BaseCommannd):
    def __init__(self):
        self.secret_token = os.environ["SECRET_KEY"]    
        
    def execute(self):
        access_token = create_access_token(identity=self.secret_token)
        return access_token

