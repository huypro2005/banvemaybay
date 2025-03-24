from src.models import Sanbay
from library import *
# from app.extension import db



def add_san_bay():
    data = request.json
    if Sanbay.query.count() >= 10:
        return jsonify({'message': 'Da dat toi da so luong san bay'})
    if data and 'ten_san_bay' in data:
        ten_san_bay = data['ten_san_bay']
        try: 
            san_bay = Sanbay(ten_san_bay = ten_san_bay)
            db.session.add(san_bay)
            db.session.commit()
            return jsonify({'message': 'San bay da duoc them'})
        except Exception as e:
            return jsonify({'message': f'Error: {e}'})
    return jsonify({'message': 'Thieu thong tin'})        
    




def get_san_bay(id):
    sanbay = Sanbay.query.get(id)
    if sanbay:
        return jsonify({'ten_san_bay': sanbay.ten_san_bay})
    return jsonify({'message': 'Khong tim thay san bay'})



def get_all_san_bay():
    try:
        sanbay = Sanbay.query.all()
        data = []
        for item in sanbay:
            data.append({
                'id': item.id,
                'ten_san_bay': item.ten_san_bay
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({'message': f'Error: {e}'})
