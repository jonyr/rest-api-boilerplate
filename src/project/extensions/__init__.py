"""
Extensions module
Each extension is initialized when app is created.
"""

from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.schema import MetaData

from .flask_schema_manager import SchemaManager
from .flask_validator_engine import ValidatorEngine
from .flask_exception_handler import ExceptionHandler
from .flask_response_manager import ResponseManager

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
schema = SchemaManager()
validator = ValidatorEngine()
catcher = ExceptionHandler()
response = ResponseManager()
