# -*- coding: utf-8 -*-
"""Flask Schema Manager."""

import importlib
from copy import deepcopy
from typing import Optional

from flask import Flask
from marshmallow import fields
from marshmallow.exceptions import ValidationError

EXTENSION_NAME = "flask-schema"


class SchemaManager(object):
    """Schema Manager."""

    def __init__(self, app: Optional[Flask] = None) -> None:
        self.errors = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize the app."""

        app.extensions = getattr(app, "extensions", {})
        app.extensions[EXTENSION_NAME] = self

        @app.teardown_appcontext
        def teardown_response_service(response_or_exc):
            self.reset()
            return response_or_exc

    def reset(self):
        """Reset the Schema Manager."""

    def get_schema_class_by_name(self, schema_class: str):
        """Get a schema class by name.

        Args:
            schema_class (str): The name of the schema class.

        Returns:
            object: The schema class.
        """

        schemas_module = importlib.import_module("src.project.schemas")
        return getattr(schemas_module, schema_class)

    def schema_class_for(self, model, name=None):
        """Get a schema class for a model.

        Args:
            model (object): The model to get the schema class for.
            name (str, optional): The name of the schema class. Defaults to None.

        Returns:
            object: The schema class.

        Raises:
            Exception: SchemaError

        """

        # Get an instance (create one if it doesn't exist)
        # And then reset it to apply all defaults

        if model is None:
            raise Exception("SchemaError")

        model_name = name or type(model).__name__

        schema_class = f"{model_name}Schema"

        return self.get_schema_class_by_name(schema_class)

    def schema_for(self, model, **kwargs):
        """Get a schema for a model.


        Args:
            model (object): The model to get the schema for.
            **kwargs: The keyword arguments to pass to the schema.

        Returns:
            object: The schema.

        Raises:
            Exception: SchemaError

        """

        name = None
        if "name" in kwargs:
            name = kwargs.pop("name")
        schema_class = self.schema_class_for(model, name=name)

        return schema_class(**kwargs)

    def dump(self, model: object, **kwargs: dict):
        """Serialize an object

        Args:
            model (object): The object to serialize.
            **kwargs: The keyword arguments to pass to the schema.

        Returns:
            dict: The serialized object.

        Raises:
            ValidationError: The validation error.

        """
        try:
            return self.schema_for(model, **kwargs).dump(model)
        except ValidationError as error:
            raise error

    def load(self, payload, name=None, **kwargs):
        """Deserialize an object.

        Args:
            payload (dict): The payload to deserialize.
            name (str, optional): The name of the schema class. Defaults to None.
            **kwargs: The keyword arguments to pass to the schema.

        Returns:
            object: The deserialized object.

        Raises:
            Exception: The validation error.

        """

        try:
            partial_nested = kwargs and ("partial_for_nested" in kwargs)
            if partial_nested:
                kwargs.pop("partial_for_nested")

            if partial_nested:
                schema = SchemaManager.partial_schema_factory(
                    self.schema_class_for(payload, name=name),
                )
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
        """Deserialize an object using a schema.

        Args:
            payload (dict): The payload to deserialize.
            schema (str): The schema class name.
            **kwargs: The keyword arguments to pass to the schema.

        Returns:
            object: The deserialized object.

        Raises:
            Exception: The validation error.

        """

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
        """Create a partial schema.

        Args:
            schema_cls (object): The schema class.

        Returns:
            object: The partial schema.
        """
        schema = schema_cls(partial=True)
        for field_name, field in schema.fields.items():
            if isinstance(field, fields.Nested):
                new_field = deepcopy(field)
                new_field.required = False
                new_field.schema.partial = True
                schema.fields[field_name] = new_field
        return schema
