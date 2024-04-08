# /models/blacklist.py
import uuid
import datetime
from sqlalchemy.dialects.postgresql import UUID
from marshmallow import Schema, fields
from ..extensions import db


# Extender la clase Model proporcionada
class BlackList(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String, unique=True, nullable=False)
    app_uuid = db.Column(UUID(as_uuid=True), nullable=False)
    blocked_reason = db.Column(db.String(255), nullable=True)
    from_ip = db.Column(db.String, nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )


class BlackListSchema(Schema):
    class Meta:
        model = BlackList
        include_relationships = False
        load_instance = True
        include_fk = True

    id = fields.Number()
    email = fields.String()
    app_uuid = fields.Number()
    blocked_reason = fields.String()
    from_ip = fields.String()
    created_at = fields.DateTime()

