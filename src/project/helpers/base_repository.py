from typing import Optional, Tuple

from flask import current_app, request
from sqlalchemy import asc, desc
from sqlalchemy.sql import text

from src.project.app import db

ORDER_OPTIONS = {"asc": asc, "desc": desc}


class BaseRepository:

    model = None

    @classmethod
    def get_model(cls):
        return cls.model

    @classmethod
    def get_polymorphic_class_names(cls) -> dict:
        subclasses = cls.model.__class__.__subclasses__(cls.model)
        polymorphic_ids = {}
        for subclass in subclasses:
            if "polymorphic_identity" in subclass.__mapper_args__:
                polymorphic_ids[subclass.__mapper_args__.get("polymorphic_identity")] = subclass.__name__
        return polymorphic_ids

    @classmethod
    def get_polymorphic_key(cls) -> Optional[str]:
        mapper_args = getattr(cls.model, "__mapper_args__", False)
        if mapper_args and ("polymorphic_on" in mapper_args):
            return getattr(mapper_args.get("polymorphic_on", {}), "key", None)
        return None

    @classmethod
    def get_polymorphic_class_name(cls, payload: dict) -> Optional[str]:
        polymorphic_key = cls.get_polymorphic_key()
        if polymorphic_key:
            if polymorphic_key in payload:
                polymorphics_class_names = cls.get_polymorphic_class_names()
                return polymorphics_class_names.get(payload[polymorphic_key], None)
        return None

    @classmethod
    def get_model_name(cls, payload: dict = None):
        subclass_name = cls.get_polymorphic_class_name(payload)
        if subclass_name:
            return subclass_name
        return getattr(cls.model, "__name__")

    @staticmethod
    def get_session():
        return db.session

    @staticmethod
    def add(obj):
        db.session.add(obj)
        return obj

    @classmethod
    def filter(
        cls,
        query=None,
        model_class=None,
        conditions: list = None,
        **kwargs,
    ):
        """
        This method return a filtered queryset based on given conditions.
            :param query: SQLAlchemy CustomBaseQuery
            :param model_class: is the model class you want to run the filter upon
            :param conditions: It is a list of tuples, ie: [(key,operator,value)]
              >>> operatorerator list:
              >>>   eq for ==
              >>>   ne for !=
              >>>   lt for <
              >>>   le for <=
              >>>   gt for >
              >>>   ge for >=
              >>>   in for in_
              >>>   is for is_
              >>>   like for like
            :param kwargs: To extend functionality

        :raise Exception: Raise this exception when:
              >>> Any filter_conditions tuple item is missing
              >>> The column does not belong to the model
              >>> The operator is not valid
        :return: filtered queryset based on given conditions.
        :rtype: CustomBaseQuery
        """

        filters = []

        try:
            request_args = request.args.to_dict(flat=True)
        except Exception:
            request_args = {}

        for condition in conditions:
            key, operator, value, source = condition
            if source == "args":
                if request_args.get(value) is not None:
                    if operator == "is":
                        filters.append((key, operator, cls.fuzzyboolean(request_args.get(value))))
                    else:
                        filters.append((key, operator, request_args.get(value)))
            elif source == "kwargs":
                if kwargs.get(key) is not None:
                    filters.append((key.replace("__", "."), operator, kwargs.get(value)))
            else:
                filters.append((key, operator, value))

        for condition in filters:
            try:
                key, operator, value = condition
            except ValueError:
                raise Exception("Invalid filter: %s" % condition) from ValueError
            column = getattr(model_class, key, None)
            if not column:
                raise Exception("Invalid filter column: %s" % key)

            if operator == "in":
                if isinstance(value, list):
                    _filter = column.in_(value)
                else:
                    _filter = column.in_(value.split(","))
            else:
                try:
                    attr = (
                        list(
                            filter(
                                lambda e: hasattr(column, e % operator),
                                ["%s", "%s_", "__%s__"],
                            )
                        )[0]
                        % operator
                    )
                except IndexError:
                    raise Exception("Invalid filter operator(): %s" % operator) from IndexError

                if value == "null":
                    value = None

                _filter = getattr(column, attr)(value)

            # add filter to sqlalchemy CustomBaseQuery

            query = query.filter(_filter)

        return query

    @classmethod
    def exists(cls, conditions: tuple) -> bool:
        """
        This method return the True if count == 1 given the conditions, otherwise False.
        :param conditions: It is a list of tuples, ie: [(key,operator,value)]
        :return: Returns true if the object exists, false if not.
        :rtype: bool
        """

        return cls.count(conditions) == 1

    @classmethod
    def first(cls, conditions: list, **kwargs: dict) -> object:
        """
        This method return the first item after filter a queryset based on given conditions.
        :param conditions: It is a list of tuples, ie: [(key,operator,value)]
        :param kwargs: Additional functionality
        :return: Returns the object instance.
        :rtype: object
        """
        model = cls.get_model()
        query = model.query
        query = cls.filter(query, model, conditions)
        query = cls.order(
            query,
            **kwargs,
        )

        return query.first()

    @classmethod
    def count(cls, conditions: list) -> int:
        """
        This method return the resultset count given the conditions.
        :param conditions: It is a list of tuples, ie: [(key,operator,value)]
        :return: Returns an integer representing the resultset count.
        :rtype: int
        """
        model = cls.get_model()
        query = model.query
        obj = cls.filter(query, model, conditions)

        return obj.count()

    @classmethod
    def get_all(cls, **kwargs) -> Tuple:
        """Returns a Tuple(resultset, Pagination)
        :returns: Tuple(List['object'], pagination)
        """

        query = cls.filter(
            cls.model.query,
            cls.model,
            cls.model.filters(),
            **kwargs,
        )
        query = cls.order(
            query,
            **kwargs,
        )
        return cls.paginate(
            query,
            **kwargs,
        )

    @staticmethod
    def get_sql_statement(query: "BaseQuery") -> str:
        """This method return a compiled query statements. Good tool for debugging"""
        return query.statement.compile(compile_kwargs={"literal_binds": True})

    @staticmethod
    def order_generation(order=None, mappings=None, custom_force=None):

        order = order or []
        mappings = mappings or {}
        ordering = []

        # Allow custom default order if not included already by the user
        if custom_force is not None:
            tmp_custom_force = custom_force.split(",")
            if "{0},desc".format(tmp_custom_force) not in order and "{0},asc".format(tmp_custom_force) not in order:
                order.append(custom_force)

        for order_item in order:
            tmp_order = order_item.split(",")

            # Validate the order and field are both valid
            if tmp_order[0] in mappings and tmp_order[1] in ORDER_OPTIONS:
                ordering.append(ORDER_OPTIONS[tmp_order[1]](mappings[tmp_order[0]]))

        return ordering

    @classmethod
    def order(cls, query, **kwargs):

        try:
            # flat=False creates a list with all the values for example
            # ?order=id,asc&order=updated_at,desc results in
            # order = ['id,asc', 'updated_at,desc']
            _order_by = request.args.to_dict(flat=False)
        except Exception:
            _order_by = {}

        order_by = _order_by.get("order", [])

        order_in_kwargs = kwargs.get("order")

        if order_in_kwargs:
            if isinstance(order_in_kwargs, list):
                order_by += order_in_kwargs
            else:
                order_by.append(order_in_kwargs)

        ordering = cls.order_generation(order_by, cls.get_model().mappings(), cls.get_model().default_order())
        return query if ordering is None else query.order_by(*ordering)

    @staticmethod
    def paginate(query, **kwargs) -> Tuple:

        pagination = None
        result = query

        max_per_page = current_app.config.get("SQLALCHEMY_DEFAULT_MAX_PER_PAGE", 100)
        default_per_page = current_app.config.get("SQLALCHEMY_DEFAULT_PER_PAGE", 25)

        try:
            request_args = request.args.to_dict()
        except Exception:
            request_args = kwargs

        if not ("all" in request_args or "all" in kwargs):
            page = 1
            per_page = default_per_page
            if kwargs.get("page", None):
                try:
                    page = int(request_args.get("page", 1))
                except (TypeError, ValueError):
                    page = 1

            if kwargs.get("per_page", None):
                try:
                    per_page = int(request_args.get("per_page", default_per_page))
                    if per_page > max_per_page:
                        per_page = max_per_page
                except (TypeError, ValueError):
                    per_page = max_per_page

            pagination = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False,
                max_per_page=max_per_page,
            )
            result = pagination.items

        return result, pagination

    @staticmethod
    def fuzzyboolean(value):
        if isinstance(value, bool):
            return value

        if not value:
            raise ValueError("boolean type must be non-null")
        value = value.lower()
        if value in (
            "false",
            "no",
            "off",
            "n",
            "0",
        ):
            return False
        if value in (
            "true",
            "yes",
            "on",
            "y",
            "1",
        ):
            return True
        raise ValueError("Invalid literal for boolean(): {}".format(value))

    @classmethod
    def run_query(cls, sql: str):
        db.session.execute(text(sql))
