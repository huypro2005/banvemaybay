from flask import Blueprint
from .services import add_san_bay, get_all_san_bay

SANBAY = Blueprint('SANBAY', __name__)

s = 'sanbay'

@SANBAY.route(f'/api/{s}/add', methods = ['POST'])
def add_san_bay_route():
    return add_san_bay()



@SANBAY.route(f'/{s}/get_all', methods = ['GET'])
def get_all_san_bay_route():
    return get_all_san_bay()


