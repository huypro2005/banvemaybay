from app.models import QuyDinh
from library import *
# from app.extension import db

def update_QuyDinh():
    try:
        rule = QuyDinh.query.first()
    except:
        return jsonify({'message': 'Co loi xay ra'}), 500
    data = request.json
    if data:
        try:
            if 'Soluongsanbay' in data:
                rule.Soluongsanbay = data['Soluongsanbay']

            if 'Thoigianbaytoithieu' in data:
                rule.Thoigianbaytoithieu = data['Thoigianbaytoithieu']  
            
            if 'Soluongsanbaytrunggian' in data:
                rule.Soluongsanbaytrunggian = data['Soluongsanbaytrunggian']

            if 'Thoigiandungtoithieu' in data:
                rule.Thoigiandungtoithieu = data['Thoigiandungtoithieu']
            
            if 'Thoigiandungtoida' in data:
                rule.Thoigiandungtoida = data['Thoigiandungtoida']
            
            if 'Phantramgia1' in data:
                rule.Phantramgia1 = data['Phantramgia1']
            
            if 'Phantramgia2' in data:
                rule.Phantramgia2 = data['Phantramgia2']

            db.session.commit()

            return jsonify({'message': 'Quy dinh da duoc cap nhat'})
        except:
            return jsonify({'message': 'Co loi xay ra'}), 500
    return jsonify({'message': 'Thieu thong tin'}), 400



def get_QuyDinh():
    try:
        rule = QuyDinh.query.first()
    except:
        return jsonify({'message': 'Co loi xay ra'}), 500
    return jsonify({'Soluongsanbay': rule.Soluongsanbay, 'Thoigianbaytoithieu': rule.Thoigianbaytoithieu, 'Soluongsanbaytrunggian': rule.Soluongsanbaytrunggian, 'Thoigiandungtoithieu': rule.Thoigiandungtoithieu, 'Thoigiandungtoida': rule.Thoigiandungtoida})
# Compare this snippet from banvemaybay/app/services_own/Quydinh/controller.py: