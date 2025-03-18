from .services import add_phieudatcho, Thanhtoan_phieudatcho_services, get_phieu_dat_cho
from flask import Blueprint, request, jsonify

phieudatcho_bp = Blueprint('phieudatcho', __name__)


@phieudatcho_bp.route('/api/phieudatcho/add', methods = ['POST'])
def add_phieudatcho_route():
    return add_phieudatcho()


@phieudatcho_bp.route('/api/phieudatcho/thanhtoan', methods = ['POST'])
def thanhtoan_phieudatcho_route():
    return Thanhtoan_phieudatcho_services()



@phieudatcho_bp.route('/api/phieudatcho/<id>', methods = ['GET'])

def get_phieu_dat_cho_route(id):
    return get_phieu_dat_cho(id)