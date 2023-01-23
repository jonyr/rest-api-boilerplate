from marshmallow import fields, validate
from src.project.models import User
from src.project.helpers.base_schema import ActiveSchema


class RegistrationSchema(ActiveSchema):
    class Meta(ActiveSchema.Meta):
        model = User

        fields = (
            "email",
            "password",
        )

    email = fields.Email(required=True, validate=validate.Length(max=150))
    password = fields.String(required=True, validate=validate.Length(min=8, max=128), load_only=True)
    name = fields.String(allow_none=True, validate=validate.Length(max=150))


class UserSchema(ActiveSchema):
    class Meta(ActiveSchema.Meta):
        model = User

        fields = (
            "email",
            "name",
            "activation_code",
            "created_at",
            "updated_at",
            "is_active",
        )

    email = fields.Email(required=True, validate=validate.Length(max=150))
    name = fields.String(allow_none=True, validate=validate.Length(max=150))
