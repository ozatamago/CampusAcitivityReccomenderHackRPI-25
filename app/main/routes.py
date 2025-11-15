# app/main/routes.py
from flask import Blueprint

# Main blueprint for basic pages (e.g., home)
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return "CampusMatching backend is running"
