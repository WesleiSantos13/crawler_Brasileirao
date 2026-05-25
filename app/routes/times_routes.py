from flask import Blueprint, jsonify
from app.services.times_service import listar_times

times_bp = Blueprint("times", __name__)

@times_bp.route("/times", methods=["GET"])
def get_times():
    return jsonify(listar_times())