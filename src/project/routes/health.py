from flask import Blueprint
from src.project.extensions import console

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    console.log("HOLA MACHO!")
    return {"status": True}, 200


@health_bp.get("/error500")
def error_500():
    2 / 0
