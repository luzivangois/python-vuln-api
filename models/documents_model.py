from sqlalchemy.dialects.postgresql import UUID
import uuid

from models import db


class Document(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(100), unique=True)
    filepath = db.Column(db.String(200))

    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath