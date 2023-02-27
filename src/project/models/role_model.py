from src.project.app import db


class Permission:
    READ = 0x01
    COMMENT = 0x02
    ADMINISTER = 0x80


class Role(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship("User", backref="role", lazy="dynamic")

    @staticmethod
    def insert_roles():
        roles = {
            "root": (0xFF, False),
            "admin": (Permission.ADMINISTER, False),
            "user": (Permission.READ | Permission.COMMENT, True),
        }

        for name in roles:
            role = Role.query.filter_by(name=name).first() or Role(name=name)
            role.permissions = roles[name][0]
            role.default = roles[name][1]
            db.session.add(role)

        db.session.commit()

    @classmethod
    def get_default_role(cls):
        """
        Returns the default role entity.

        :param email: Email
        :type email: str
        :return: User instance
        """
        return cls.query.filter(cls.default.is_(True)).first()
