from typing import List, Union

from flask import request
from flask_jwt_extended import get_jwt

from src.project.app import schema, db
from src.project.exceptions import CustomException


class BaseService:
    """A class used as a base for any services"""

    repository = None

    @classmethod
    def get_repository(cls) -> object:
        """Return service associated repository instance"""
        return cls.repository

    @classmethod
    def get_model_name(cls, payload) -> str:
        return cls.repository.get_model_name(payload)

    @classmethod
    def get_entity_name(cls) -> str:
        return cls.repository.get_model_name().replace("Model", "")

    @classmethod
    def deserialize(cls, payload: dict, **extra_attributes: dict) -> object:
        """Deserialize a data structure to an object defined by this SchemaManagerhema’s fields."""
        obj = schema.load(payload, name=cls.get_model_name(payload), **extra_attributes)
        # obj = schema.load(payload, name=schema, **extra_attributes)
        cls.repository.add(obj)
        return obj

    @classmethod
    def deserialize_for(cls, obj_class: object, payload: dict, **extra_attributes: dict) -> object:
        """Deserialize a data structure to an object defined by this SchemaManagerhema’s fields."""
        obj = schema.load(payload, name=getattr(obj_class, "__name__"), **extra_attributes)
        cls.repository.add(obj)
        return obj

    @classmethod
    def deserialize_using(cls, payload: dict, schema_name, **extra_attributes: dict):
        obj = schema.load_using(payload, schema_name, **extra_attributes)
        cls.repository.add(obj)
        return obj

    @classmethod
    def post(cls, payload: dict = None, commit: bool = True, **kwargs) -> object:
        """Add a new object and persist it to DB

        :param payload: An object python dict representation
        :param commit: commit the transaction
        :param kwargs: extra parameters
        :returns: object
        """
        payload = payload or request.get_json()
        obj = cls.deserialize(payload, **kwargs)
        obj.before_post()

        if commit:
            db.session.commit()

        return obj

    @classmethod
    def put(cls, instance: object, payload: dict = None, commit: bool = True, **kwargs) -> object:
        """Update an object and persist it to DB

        :param instance: An object instance
        :param payload: An object python dict representation
        :param commit: commit the transaction
        :param kwargs: extra parameters
        :returns: object
        """
        payload = payload or request.get_json()
        obj = cls.deserialize(payload, instance=instance, **kwargs)
        obj.before_put()

        if commit:
            db.session.commit()
        return obj

    @classmethod
    def patch(cls, instance: object, payload: dict = None, commit: bool = True, **kwargs) -> object:
        """Update an user and persist it to DB

        :param instance: An object instance
        :param payload: An object python dict representation
        :param commit: commit the transaction
        :param kwargs: extra parameters
        :returns: object
        """
        payload = payload or request.get_json()

        obj = cls.deserialize(payload, instance=instance, partial=True, unknown="exclude", **kwargs)
        obj.before_patch()

        if commit:
            cls.commit()

        return obj

    @classmethod
    def delete(cls, instance: object, commit=True) -> None:
        """Update an object and persist it to DB

        :param instance: An object instance
        """
        instance.delete()
        if commit:
            db.session.commit()

    @classmethod
    def get_by_id(cls, obj_id: int) -> object:  # pylint: disable=unused-argument
        """Get an object by its id or raise a ResourceNotFoundError if None
        :param obj_id: The object unique identifier.
        :raises ResourceNotFoundError:
        :return: Returns an object instance or raise a ResourceNotFoundError if None
        """

        conditions = [
            ("id", "eq", obj_id, "default"),
            ("is_deleted", "is", False, "default"),
        ]

        obj = cls.repository.first(conditions)

        if not obj:
            raise CustomException(f"Resource with id {obj_id} not found", "ResourceNotFound", 404)

        return obj

    @classmethod
    def get_by(cls, conditions: list = None, exclude_deleted: bool = True, **kwargs) -> object:
        """Get an object by given filters or raise a ResourceNotFoundError if None
        :param conditions: A tuple ('field', 'comparison op', 'value', 'where to get the value')
        :param exclude_deleted: filter not logically deleted objects
        :param kwargs: Extend functionality
        :raises ResourceNotFoundError:
        :return: Returns an object instance or raise a ResourceNotFoundError if None
        """

        internal_filters = (
            []
            if not exclude_deleted
            else [
                (
                    "is_deleted",
                    "is",
                    False,
                    "default",
                )
            ]
        )

        if conditions:
            internal_filters += conditions

        obj = cls.repository.first(internal_filters, **kwargs)

        if not obj:
            raise CustomException("Resource not found", "ResourceNotFound", 404)

        return obj

    @classmethod
    def get_deleted_by(cls, conditions: list = None) -> object:
        """Get an object by given filters or raise a ResourceNotFoundError if None
        :param conditions: A tuple ('field', 'comparison op', 'value', 'where to get the value')
        :return: Returns an object instance or None
        """

        internal_filters = [
            (
                "is_deleted",
                "is",
                True,
                "default",
            )
        ]

        if conditions:
            internal_filters += conditions

        return cls.repository.first(internal_filters)

    @classmethod
    def get_all(cls, **kwargs):
        return cls.repository.get_all(**kwargs)

    @classmethod
    def count(cls, conditions: List) -> int:
        return cls.repository.count(conditions)

    @staticmethod
    def check_permissions(key, value):
        claims = get_jwt()
        attribute = claims.get(key, None)

        if attribute != value:
            raise CustomException()

    @classmethod
    def references_dict(cls, field="name") -> Union[dict, None]:
        """Gets a dictionary."""
        if hasattr(cls.repository.model, field):
            items, _ = cls.repository.get_all(all=True, is_active=True)
            return {item.id: getattr(item, field) for item in items.all()}

        return None

    @staticmethod
    def commit():
        db.session.commit()

    @staticmethod
    def flush():
        db.session.flush()

    @classmethod
    def validate_foreign_key(cls, obj_id: int):
        if not cls.repository.count(conditions=[("id", "eq", obj_id, "default")]):
            raise CustomException(
                f"Resource with id {obj_id} not found. ({cls.get_entity_name()})",
                "ResourceNotFound",
                404,
            )

    @staticmethod
    def find_by_id(obj_list: list, obj_id: int) -> Union[object, None]:
        """Find object in list by id.
        :param obj_list: a list of instances
        :param obj_id: object id
        :return: Returns an object instance or None"""
        try:
            return next((item for item in obj_list if item.id == obj_id), None)
        except AttributeError:
            return None

        return None
