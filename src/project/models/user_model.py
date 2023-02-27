from datetime import datetime
import pytz

from sqlalchemy import and_
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.security import check_password_hash, generate_password_hash

from src.project.app import db
from src.project.exceptions import CustomException
from src.project.helpers import random_num, encode_object, decode_string, get_ip_address


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128))
    activation_code = db.Column(db.String(10))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # Activity Tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, server_default=db.func.now())
    current_sign_in_ip = db.Column(db.String(45))
    last_sign_in_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    last_sign_in_ip = db.Column(db.String(45))

    is_active = db.Column(db.BOOLEAN, default=False, server_default="0", index=True)
    is_deleted = db.Column(db.BOOLEAN, default=False, server_default="0")

    extra_attributes = db.Column(db.JSON, default=None)

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(User, self).__init__(**kwargs)
        self.email = kwargs.get("email", "").lower()
        self.password = self.encrypt_password(kwargs.get("password", ""))
        self.activation_code = random_num(6)

    @staticmethod
    def encrypt_password(password: str):
        """
        Hash a plaintext string using PBKDF2. This is good enough according
        to the NIST (National Institute of Standards and Technology).

        In other words while bcrypt might be superior in practice, if you use
        PBKDF2 properly (which we are), then your passwords are safe.

        :param password: Password in plain text
        :type password: str
        :return: str
        """
        return generate_password_hash(password) if password else None

    @classmethod
    def find_by_email(cls, email: str):
        """
        Finds a user by their e-mail.

        :param email: Email
        :type email: str
        :return: User instance
        """
        return cls.query.filter(and_(cls.email == email.lower()), cls.is_deleted.is_(False)).first()

    @classmethod
    def find_by_id(cls, user_id: int):
        """
        Finds a user by their id.

        :param user_id: User id
        :type user_id: int
        :return: User instance
        """
        return cls.query.filter(cls.id == user_id).first()

    def authenticated(self, with_password: bool = True, password: str = ""):
        """
        Ensure a user is authenticated, and optionally check their password.

        :param with_password: Optionally check their password
        :type with_password: bool
        :param password: Optionally verify this as their password
        :type password: str
        :return: bool
        """
        if with_password:
            return self.check_password(password)

        return True

    def check_password(self, password: str) -> bool:
        """
        Compare clean and hashed password.

        Returns `True` if the password matched, `False` otherwise.
        """
        return check_password_hash(self.password, password)

    def activation_code_expired(self) -> bool:
        """
        Checks if the activation code has expired.
        """
        now = datetime.now(tz=pytz.UTC)
        seconds = (now - self.updated_at).total_seconds()

        return seconds > 60 * 60 * 24

    def clean_activation_code(self):
        self.activation_code = None
        self.updated_at = datetime.utcnow()

    def validate_activation_code(self, code):

        if self.activation_code != str(code):
            raise CustomException("Invalid code", "InvalidActivationCodeError")

        if self.activation_code_expired():
            raise CustomException("Activation code has expired", "ExpiredActivationCodeError")

        self.clean_activation_code()
        self.enable()

        return True

    def update_activity_tracking(self, ip_address=None):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address or get_ip_address()

        return self.save()

    def reset_activation_code(self):
        self.activation_code = random_num(6)
        self.before_put()
        return self.save()

    def enable(self):
        self.is_active = True

    def disable(self):
        self.is_active = True

    def toogle(self):
        self.is_active = not self.is_active

    def delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.datetime.utcnow()

    def undelete(self):
        self.is_deleted = False
        self.deleted_at = None

    # Hooks #

    def before_post(self):
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()
        self.email = self.email.lower()

    def before_put(self):
        self.updated_at = datetime.datetime.utcnow()

    def before_patch(self):
        self.updated_at = datetime.datetime.utcnow()

    def before_delete(self):
        self.deleted_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)

        if self.extra_attributes:
            flag_modified(self, "extra_attributes")

        db.session.commit()

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
        return [
            ("is_deleted", "is", False, "default"),
            ("is_active", "is", "is_active", "args"),
            ("is_active", "is", "is_active", "kwargs"),
            ("id", "in", "id", "args"),
            ("id", "in", "id", "kwargs"),
            ("email", "eq", "email", "args"),
            ("email", "eq", "email", "kwargs"),
        ]

    def __repr__(self):
        return f"<User {self.first_name} [{self.id}]>"

    def encode(self):
        return encode_object({"id": self.id})
