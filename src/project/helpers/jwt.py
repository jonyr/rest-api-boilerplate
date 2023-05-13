from typing import Any
from src.project.extensions import jwt, rediscache, api


def register_jwt_handlers():
    """
    Registers handlers for jwt_extended.
    """

    @jwt.invalid_token_loader
    def my_expired_token_callback(error):
        """
        The authorization token is not valid or it was altered.
        """

        return api.error(
            {
                "code": "InvalidTokenError",
                "description": error,
            },
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """
        On expired token, raise ExpiredToken 401

        jwt_header {'typ': 'JWT', 'alg': 'HS256'}
        jwt_payload {
            'fresh': True,
            'iat': 1620145309,
            'jti': 'c8041f8f-4af6-41b4-80c2-c611be793839',
            'type': 'access',
            'sub': 1,
            'nbf': 1620145309,
            'exp': 1620145310,
            }
        """
        return api.error(
            {
                "code": "ExpiredTokenError",
                "description": "I can't let you do that",
            },
            code=401,
        )

    @jwt.unauthorized_loader
    def unauthorized_loader_callback(error: Any):
        """
        Missing authorization token header.
        """
        return api.error(
            {
                "code": "MissingTokenError",
                "description": error,
            },
            code=401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """
        On revoked token, raise RevokedToken 401

        Args:
            jwt_header (dict): JWT header
            jwt_payload (dict): JWT payload

        Returns:
            dict: Error response
        """

        return api.error(
            {
                "code": "RevokedTokenError",
                "description": "The Token is revoked",
            },
            code=401,
        )

    # Callback function to check if a JWT exists in the redis blocklist
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token_in_redis = rediscache.get(jti)

        return token_in_redis is not None
