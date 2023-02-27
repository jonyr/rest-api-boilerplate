from flask import Blueprint, current_app
from jinja2 import Environment, PackageLoader

from src.project.app import response
from src.project.helpers import get_default_email_template_params

toolbox_bp = Blueprint("toolbox", __name__)

env = Environment(loader=PackageLoader("src.project", "templates"))


@toolbox_bp.get("/toolbox")
def toolbox():
    return response.build({"status": True})


@toolbox_bp.get("/toolbox/templates")
def email_templates():

    template = env.get_template("emails/base.html")

    # GREEN "PRIMARY_COLOR": "#1ca72c",

    context = {
        **get_default_email_template_params(),
        "TITLE": "Activate your account",
        "BODY": "Hello,<br>please activate your account inmediatly.",
        "CTA_TEXT": "Activate account",
        "CTA_LINK": "https://app.morfi.pro",
    }

    return template.render(context)
