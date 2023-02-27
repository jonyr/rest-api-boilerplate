from marshmallow import fields, validate, post_load

from src.project.app import ma
from src.project.helpers.base_schema import ActiveSchema
from src.project.models import User


class RegistrationSchema(ActiveSchema):
    class Meta(ActiveSchema.Meta):
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
        )

    email = fields.Email(required=True, validate=validate.Length(max=150))
    password = fields.String(required=True, validate=validate.Length(min=8, max=128), load_only=True)
    first_name = fields.String(allow_none=False, validate=validate.Length(max=50))
    last_name = fields.String(allow_none=True, missing=None, validate=validate.Length(max=50))


class UserSchema(ActiveSchema):
    class Meta(ActiveSchema.Meta):
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "extra_attributes",
            "last_sign_in_at",
            "last_sign_in_ip",
            "current_sign_in_ip",
            "current_sign_in_at",
            "created_at",
            "updated_at",
            "sign_in_count",
        )


class LoginSchema(ma.Schema):
    class Meta:
        ordered = True

        fields = (
            "email",
            "password",
        )

    email = fields.Email(required=True, validate=validate.Length(max=150))
    password = fields.String(required=True, validate=validate.Length(max=128, min=8))

    @post_load
    def lower_email(self, in_data, **kwargs):
        in_data["email"] = in_data["email"].lower()
        return in_data
