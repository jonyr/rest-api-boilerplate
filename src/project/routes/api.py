from flask import Blueprint, request
from src.project.models import User

api_bp = Blueprint("users", __name__, url_prefix="/api")


@api_bp.get("/users")
def get_data():
    """
    Get data for the DataTables table.
    """
    search = request.args.get("search", None)
    sort = request.args.get("sort", None)
    start = request.args.get("start", type=int, default=-1)
    length = request.args.get("length", type=int, default=-1)

    return User.get_data(**request.args)
