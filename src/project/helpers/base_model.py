from datetime import datetime

# from flask_babel import format_datetime

from src.project.app import db


class BaseModel(object):
    """
    Base model for all models to inherit from.
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_deleted = db.Column(db.BOOLEAN, default=False, server_default="0")

    def delete(self):
        """
        Soft delete the instance.
        """
        self.is_deleted = True

    def undelete(self):
        """
        Undelete the instance.
        """
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
        """
        Returns a list of tuples with the following format:
        (column, operator, value, source)
        """
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
        """
        Returns a dictionary representation of the model.
        """
        if hasattr(self, "__table__"):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class AuditModel(BaseModel):
    """
    Audit model for all models to inherit from.
    """

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        index=True,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.datetime.utcnow,
        index=True,
    )

    deleted_at = db.Column(
        db.DateTime(timezone=True),
    )

    def delete(self):
        """
        Soft delete the instance.
        """
        super().delete()
        self.deleted_at = datetime.datetime.utcnow()

    def undelete(self):
        """
        Undelete the instance.
        """
        super().undelete()
        self.deleted_at = None

    def before_post(self):
        """
        Hook to run before a model is created.
        """
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def before_put(self):
        """
        Hook to run before a model is updated.
        """
        self.updated_at = datetime.datetime.utcnow()

    def before_patch(self):
        """
        Hook to run before a model is patched.
        """
        self.updated_at = datetime.datetime.utcnow()

    def before_delete(self):
        """
        Hook to run before a model is deleted.
        """
        self.deleted_at = datetime.datetime.utcnow()


class ActiveModel(object):
    """
    Active model for all models to inherit from.
    """

    is_active = db.Column(db.BOOLEAN, default=True, server_default="1", index=True)

    def toggle(self):
        """
        Toggle the active state of the instance.
        """
        self.is_active = not self.is_active

    def enable(self):
        """
        Enable the instance.
        """
        self.is_active = True

    def disable(self):
        """
        Disable the instance.
        """
        self.is_active = False
