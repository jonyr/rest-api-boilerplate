from marshmallow import fields
from src.project.app import db, ma


class BaseSchema(ma.SQLAlchemyAutoSchema):  # pylint: disable=inherit-non-class
    class Meta:
        session = db.session
        load_instance = True
        include_relationships = True
        ordered = True


class ActiveSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        fields = (
            "is_active",
            "updated_at",
            "created_at",
            "deleted_at",
        )

    is_active = fields.Boolean()
    created_at = fields.DateTime("%Y-%m-%dT%H:%M:%S+00:00", dump_only=True)
    updated_at = fields.DateTime("%Y-%m-%dT%H:%M:%S+00:00", dump_only=True)
    deleted_at = fields.DateTime("%Y-%m-%dT%H:%M:%S+00:00", dump_only=True)
