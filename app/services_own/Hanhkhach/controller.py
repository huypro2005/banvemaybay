from flask import Blueprint
from .services import add_hanh_khach

HANHKHACH = Blueprint('HANHKHACH', __name__)

s = 'hanhkhach'

@HANHKHACH.route(f'/{s}/add', methods = ['POST'])
def add_san_bay_route():
    return add_hanh_khach()



# @HANHKHACH.route(f'/{s}/get_all', methods = ['GET'])
# def get_all_san_bay_route():
#     return get_all_san_bay()