from .services import get_ve_chuyen_bay, add_ve_cb, update_tinhtrang_daban, update_tinhtrang_dahuy
from flask import Blueprint, request, jsonify

vechuyenbay_bp = Blueprint('vechuyenbay', __name__)

@vechuyenbay_bp.route('/api/vechuyenbay/<id>', methods = ['GET'])
def get_ve_chuyen_bay_route(id):
    return get_ve_chuyen_bay(id)


