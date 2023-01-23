from datetime import datetime

from sqlalchemy import and_
from werkzeug.security import check_password_hash, generate_password_hash

from src.project.app import db
from src.project.helpers import random_num, verify_token


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, server_default=db.func.now())
    deleted_at = db.Column(db.DateTime(timezone=True))
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128))
    activation_code = db.Column(db.String(10))

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
        return cls.query.filter(and_(cls.email == email), cls.is_deleted.is_(False)).first()

    @classmethod
    def find_by_id(cls, user_id: int):
        """
        Finds a user by their id.

        :param user_id: User id
        :type user_id: int
        :return: User instance
        """
        return cls.query.filter(cls.id == user_id).first()

    @classmethod
    def find_by_token(cls, token: str, expiration: int = 3600):
        """
        Obtains a user by looking up their email contained in a token.

        :param token: Signed token.
        :type token: str
        :param expiration: Seconds until it expires, defaults to 1 hour
        :type expiration: int
        :return: User instance or None
        """
        email = verify_token(token, expiration)

        return User.find_by_identity(email) if email else None

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
        now = datetime.utcnow()
        seconds = (now - self.updated_at).total_seconds()

        return seconds > 60 * 15

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
        return f"<User {self.name} [{self.id}]>"
