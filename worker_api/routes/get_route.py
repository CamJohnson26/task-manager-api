# routes/get_route.py

from flask import Blueprint, render_template

get_route_bp = Blueprint('home', __name__)


@get_route_bp.route('/')
def get_route():
    return "Hello World!"