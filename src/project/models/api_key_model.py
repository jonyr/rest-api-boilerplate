from src.project.extensions import db


class ApiKey(db.Model):

    __tablename__ = "api_keys"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    is_active = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    @classmethod
    def mappings(cls):
        return {"id": cls.id}

    @staticmethod
    def default_order():
        return "id,desc"

    @classmethod
    def filters(cls):
        return [
            ("is_active", "is", "is_active", "kwargs"),
            ("id", "in", "id", "args"),
            ("id", "in", "id", "kwargs"),
        ]
