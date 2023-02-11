from flask import Blueprint, request

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    return {"status": True}, 200


@health_bp.get("/test")
def test():

    args = request.args.to_dict(flat=False)

    return {}, 200
