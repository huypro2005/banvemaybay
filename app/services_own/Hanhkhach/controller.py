from flask import Blueprint
from .services import add_hanh_khach, get_hanhkhach_by_cmnd

HANHKHACH = Blueprint('HANHKHACH', __name__)

s = 'hanhkhach'

@HANHKHACH.route(f'/{s}/add', methods = ['POST'])
def add_san_bay_route():
    return add_hanh_khach()


@HANHKHACH.route(f'/{s}/get_by_cmnd/<cmnd>', methods = ['GET'])
def get_hanhkhach_by_cmnd_route(cmnd):
    return get_hanhkhach_by_cmnd(cmnd)




# @HANHKHACH.route(f'/{s}/get_all', methods = ['GET'])
# def get_all_san_bay_route():
#     return get_all_san_bay()