from models import ChiTietChuyenBay, Chuyenbay, Sanbay
from library import *
from extension import db

def add_chi_tiet_chuyen_bay():
    data = request.json
    if data and 'ma_chuyen_bay' in data and 'ma_san_bay_tg' in data and 'Thoi_gian_dung' in data and 'ghi_chu' in data:
        ma_chuyen_bay = data['ma_chuyen_bay']
        ma_san_bay = data['ma_san_bay_tg']
        thoi_gian_dung = data['Thoi_gian_dung']
        ghi_chu = data['ghi_chu']

        # Thoi gian dung phai lon hon 0 va nho hon 20
        if thoi_gian_dung < 0:
            return jsonify({'message': 'Thoi gian dung phai lon hon 0'})
        if thoi_gian_dung > 20:
            return jsonify({'message': 'Thoi gian dung phai nho hon 20'})
        chuyenbay = Chuyenbay.query.get(ma_chuyen_bay)
        sanbay = Sanbay.query.get(ma_san_bay)

        # Ma chuyen bay va ma san bay phai ton tai
        if not chuyenbay or not sanbay:
            return jsonify({'message': 'Ma chuyen bay hoac ma san bay khong ton tai'})
        
        # San bay trung gian phai khac san bay di va san bay den
        if chuyenbay.Ma_san_bay_di == ma_san_bay or chuyenbay.Ma_san_bay_den == ma_san_bay:
            return jsonify({'message': 'San bay trung gian phai khac san bay di va san bay den'})
        
        # Chi co toi da 2 san bay trung gian
        if ChiTietChuyenBay.query.filter(ma_chuyen_bay).count()>=2:
            return jsonify({'message': 'Chuyen bay da co toi da 2 san bay trung gian'})
        try:
            thu_tu_tg = ChiTietChuyenBay.query.filter(ma_chuyen_bay).count() + 1
            chi_tiet_chuyen_bay = ChiTietChuyenBay(Ma_chuyen_bay = ma_chuyen_bay, Ma_san_bay = ma_san_bay, Thoi_gian_dung = thoi_gian_dung, Thu_tu_TG = thu_tu_tg, Ghi_chu = ghi_chu)
            db.session.add(chi_tiet_chuyen_bay)
            db.session.commit()
            return jsonify({'message': 'Chi tiet chuyen bay da duoc them'})
        except:
            return jsonify({'message': 'Co loi xay ra'})
        
    return jsonify({'message': 'Thieu thong tin'})


def get_chi_tiet_chuyen_bay(id):
    chi_tiet_chuyen_bay = ChiTietChuyenBay.query.get(id)
    if chi_tiet_chuyen_bay:
        return jsonify({'Ma_chuyen_bay': chi_tiet_chuyen_bay.Ma_chuyen_bay, 'Ma_san_bay': chi_tiet_chuyen_bay.Ma_san_bay, 'Thoi_gian_dung': chi_tiet_chuyen_bay.Thoi_gian_dung, 'Thu_tu_TG': chi_tiet_chuyen_bay.Thu_tu_TG, 'Ghi_chu': chi_tiet_chuyen_bay.Ghi_chu})
    return jsonify({'message': 'Khong tim thay chi tiet chuyen bay'})