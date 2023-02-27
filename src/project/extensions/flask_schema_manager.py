import importlib
from copy import deepcopy
from typing import Optional

from flask import Flask
from marshmallow import fields
from marshmallow.exceptions import ValidationError

EXTENSION_NAME = "flask-schema"


class SchemaManager(object):
    def __init__(
        self,
        app: Optional[Flask] = None,
    ) -> None:

        self.errors = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.app = app

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

    def reset(self):
        pass

    def get_schema_class_by_name(self, schema_class: str):
        # Get a schema
        # And then reset it to apply all defaults

        schemas_module = importlib.import_module("src.project.schemas")
        return getattr(schemas_module, schema_class)

    def schema_class_for(self, model, name=None):
        # Get an instance (create one if it doesn't exist)
        # And then reset it to apply all defaults

        if model is None:
            raise Exception("SchemaError")

        model_name = name or type(model).__name__

        schema_class = f"{model_name}Schema"

        return self.get_schema_class_by_name(schema_class)

    def schema_for(self, model, **kwargs):
        # Get an instance (create one if it doesn't exist)
        # And then reset it to apply all defaults
        name = None
        if "name" in kwargs:
            name = kwargs.pop("name")
        schema_class = self.schema_class_for(model, name=name)

        return schema_class(**kwargs)

    def dump(self, model: object, **kwargs: dict):
        """Serialize an object"""
        try:
            return self.schema_for(model, **kwargs).dump(model)
        except ValidationError as error:
            raise error

    def load(self, payload, name=None, **kwargs):
        try:
            partial_nested = kwargs and ("partial_for_nested" in kwargs)
            if partial_nested:
                kwargs.pop("partial_for_nested")

            if partial_nested:
                schema = SchemaManager.partial_schema_factory(self.schema_class_for(payload, name=name))
            else:
                schema = self.schema_for(payload, name=name, **kwargs)

            # kwargs 'many', 'partial' or 'unknown' must to be passed to load
            load_kwargs = {
                key: value
                for key, value in kwargs.items()
                if key
                in (
                    "instance",
                    "many",
                    "partial",
                    "unknown",
                )
            }

            if kwargs.get("context"):
                schema.context = kwargs.get("context")

            return schema.load(payload, **load_kwargs)
        except ValidationError as error:
            message = error.normalized_messages()
            raise Exception(
                description="Schema validation error",
                messages=message,
            ) from error

    def load_using(self, payload, schema, **kwargs):
        try:

            schema_class = self.get_schema_class_by_name(schema)

            schema = schema_class(**kwargs)

            # kwargs 'many', 'partial' or 'unknown' must to be passed to load
            load_kwargs = {
                key: value
                for key, value in kwargs.items()
                if key
                in (
                    "instance",
                    "many",
                    "partial",
                    "unknown",
                )
            }

            if kwargs.get("context"):
                schema.context = kwargs.get("context")

            return schema.load(payload, **load_kwargs)
        except ValidationError as error:
            message = error.normalized_messages()
            raise Exception(
                description="Schema validation error",
                messages=message,
            ) from error

    @staticmethod
    def partial_schema_factory(schema_cls):
        schema = schema_cls(partial=True)
        for field_name, field in schema.fields.items():
            if isinstance(field, fields.Nested):
                new_field = deepcopy(field)
                new_field.required = False
                new_field.schema.partial = True
                schema.fields[field_name] = new_field
        return schema
