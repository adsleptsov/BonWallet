from flask import Blueprint

rewards_bp = Blueprint(
        "rewards",
        __name__,
        url_prefix="/rewards",
        template_folder="templates",
        static_folder="static"
    )

from server.posts import routes
