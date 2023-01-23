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
            "created_at_tz",
            "updated_at_tz",
        )

    is_active = fields.Boolean(data_key="isActive")
    created_at = fields.DateTime(
        "%Y-%m-%dT%H:%M:%S+00:00", dump_only=True, data_key="createdAt"
    )
    updated_at = fields.DateTime(
        "%Y-%m-%dT%H:%M:%S+00:00", dump_only=True, data_key="updatedAt"
    )
    deleted_at = fields.DateTime(
        "%Y-%m-%dT%H:%M:%S+00:00", dump_only=True, data_key="deletedAt"
    )
    updated_at_tz = fields.String(dump_only=True, data_key="updatedAtTz")
    created_at_tz = fields.String(dump_only=True, data_key="createdAtTz")
