from flask import Blueprint, request
from src.project.helpers.decorators import requires_api_key

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    return {"status": True}, 200
