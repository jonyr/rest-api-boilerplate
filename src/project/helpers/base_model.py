from datetime import datetime

# from flask_babel import format_datetime

from src.project.app import db


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_deleted = db.Column(db.BOOLEAN, default=False, server_default="0")

    def delete(self):
        self.is_deleted = True

    def undelete(self):
        self.is_deleted = False

    @classmethod
    def mappings(cls):
        return {
            "id": cls.id,
            "created_at": cls.created_at,
            "updated_at": cls.updated_at,
        }

    @staticmethod
    def default_order():
        return "id,desc"

    @classmethod
    def filters(cls):
        return [
            ("is_deleted", "is", False, "default"),
            ("is_active", "is", "is_active", "args"),
            ("is_active", "is", "is_active", "kwargs"),
            ("id", "in", "id", "args"),
            ("id", "in", "id", "kwargs"),
        ]

    @classmethod
    def joins(cls):
        return []

    def as_dict(self):
        """Returns instance as a python dictionary."""
        if hasattr(self, "__table__"):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AuditModel(BaseModel):
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.utcnow, index=True
    )
    updated_at = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.utcnow, index=True
    )
    deleted_at = db.Column(db.DateTime(timezone=True))

    def delete(self):
        super().delete()
        self.deleted_at = datetime.datetime.utcnow()

    def undelete(self):
        super().undelete()
        self.deleted_at = None

    def before_post(self):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def before_put(self):
        self.updated_at = datetime.datetime.utcnow()

    def before_patch(self):
        self.updated_at = datetime.datetime.utcnow()

    def before_delete(self):
        self.deleted_at = datetime.datetime.utcnow()

    @property
    def created_at_tz(self):
        pass
        # return format_datetime(self.created_at, format="short")

    @property
    def updated_at_tz(self):
        pass
        # return format_datetime(self.updated_at, format="short")


class ActiveModel(object):
    is_active = db.Column(db.BOOLEAN, default=True, server_default="1", index=True)

    def toggle(self):
        self.is_active = not self.is_active

    def enable(self):
        self.is_active = True

    def disable(self):
        self.is_active = False
