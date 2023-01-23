from flask import Blueprint, render_template

apidoc_bp = Blueprint(
    "apidoc",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/apidoc",
)


@apidoc_bp.route("/apidoc")
def index():
    return render_template("index.jinja")
