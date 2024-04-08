from .base_command import BaseCommannd
from ..errors.errors import ResetBlackListDBError
from ..models.blacklist import BlackList
from ..extensions import db


class ViewBlackListReset(BaseCommannd):
    def execute(self):
        try:
            BlackList.query.delete()
            db.session.commit()
            return {"msg": "Todos los datos fueron eliminados"}
        except Exception:
            db.session.rollback()
            raise ResetBlackListDBError
