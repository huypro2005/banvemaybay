from flask import Blueprint
from .services import add_Maybay

MAYBAY = Blueprint('MAYBAY', __name__)

s = 'maybay'

@MAYBAY.route(f'/api/{s}/add', methods = ['POST'])
def add_san_bay_route():
    return add_Maybay()



# @MAYBAY.route(f'/{s}/get_all', methods = ['GET'])
# def get_all_san_bay_route():
#     return get_all_san_bay()