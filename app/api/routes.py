# app/api/routes.py
from flask import Blueprint, jsonify

# API blueprint for JSON endpoints
api_bp = Blueprint("api", __name__)

@api_bp.route("/ping")
def ping():
    return jsonify({"message": "pong"})
