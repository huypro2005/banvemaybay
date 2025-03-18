from flask import Blueprint, request, jsonify
from .services import update_QuyDinh, get_QuyDinh

QUYDINH = Blueprint('QUYDINH', __name__)
s = 'quydinh'

@QUYDINH.route(f'/{s}/update', methods = ['POST'])
def update_QuyDinh_route():
    return update_QuyDinh()

@QUYDINH.route(f'/{s}/get', methods = ['GET'])
def get_QuyDinh_route():
    return get_QuyDinh()
