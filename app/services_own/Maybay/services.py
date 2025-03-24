# from extension import db
from app.models import Maybay
from library import *

def add_Maybay():
    data = request.json
    if data and 'ten_may_bay' in data:
        ten_may_bay = data['ten_may_bay']
        try:
            maybay = Maybay(ten_may_bay= ten_may_bay)
            db.session.add(maybay)
            db.session.commit()
            return jsonify({'message': 'Add success!'})
        except Exception as e:
            return jsonify({'message': f'Error: {e}'})
    return jsonify({'message': 'request fail'})



def get_Maybay():
    try:
        ds = Maybay.query.all()
        data = []
        for item in ds:
            data.append({
                'id': item.id,
                'ten_may_bay': item.ten_may_bay
            })
        return jsonify(data)
    except Exception as e:
        return jsonify({'message': f'Error: {e}'})
