from .services import get_ve_chuyen_bay, add_ve
from flask import Blueprint, request, jsonify

vechuyenbay_bp = Blueprint('vechuyenbay', __name__)

@vechuyenbay_bp.route('/api/vechuyenbay/<id>', methods = ['GET'])
def get_ve_chuyen_bay_route(id):
    return get_ve_chuyen_bay(id)



@vechuyenbay_bp.route('/api/vechuyenbay/add', methods = ['POST'])

def add_ve_route():
    return add_ve()