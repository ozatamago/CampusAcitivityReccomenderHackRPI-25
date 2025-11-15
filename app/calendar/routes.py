# app/calendar/routes.py
from flask import Blueprint, jsonify

# Calendar blueprint for Google Calendar integration
calendar_bp = Blueprint("calendar", __name__)

@calendar_bp.route("/ping")
def ping_calendar():
    return jsonify({"message": "calendar ok"})
