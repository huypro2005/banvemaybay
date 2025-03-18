from app.services.lichchuyenbay_service import add_chuyen_bay
from flask import Blueprint, request, jsonify

chuyenbay_bp = Blueprint('chuyenbay', __name__)

@chuyenbay_bp.route('/api/chuyenbay/add', methods = ['POST'])
def add_chuyen_bay_route():
    return add_chuyen_bay()