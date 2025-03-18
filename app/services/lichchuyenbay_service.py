from app.models import Chuyenbay, ChiTietChuyenBay, QuyDinh
from app import db
from datetime import datetime
from library import *

def add_chuyenbay():
    try:
        rule = QuyDinh.query.first()
    except:
        return jsonify({'message': 'Lỗi'}), 400
    try:
        data = request.get_json()
        tmp = ['Ma_chuyen_bay', 'Ma_san_bay_di', 'Ma_san_bay_den', 'Ma_may_bay', 'gia_ve', 'thoi_gian_bay', 'so_ghe_hang1', 'so_ghe_hang2']
        if data is None or not all(k in data for k in tmp):
            return jsonify({'message': 'Thiếu thông tin'}), 400
        ma_chuyen_bay = data['Ma_chuyen_bay']
        ma_san_bay_di = data['Ma_san_bay_di']
        ma_san_bay_den = data['Ma_san_bay_den']
        ma_may_bay = data['Ma_may_bay']
        gia_ve = data['gia_ve']
        ngay_gio_str = data['ngay_gio']
        thoi_gian_bay = data['thoi_gian_bay']
        so_ghe_hang1 = data['so_ghe_hang1']
        so_ghe_hang2 = data['so_ghe_hang2']
        tongsoghe = so_ghe_hang1 + so_ghe_hang2
        cb = Chuyenbay.query.get(ma_chuyen_bay)
        if cb:
            return jsonify({'message': 'Mã chuyến bay đã tồn tại'}), 400
        if so_ghe_hang1 < 0 or so_ghe_hang2 < 0:
            return jsonify({'message': 'Số ghế không hợp lệ'}), 400
        
        if thoi_gian_bay < rule.Thoigianbaytoithieu:
            return jsonify({'message': f'Thời gian bay phải lớn hơn {rule.Thoigianbaytoithieu} phút'}), 400

        if ma_san_bay_den == ma_san_bay_di:
            return jsonify({'message': 'Mã sân bay đi và đến không được trùng'}), 400
        
        try:
            # Dùng datetime.strptime để chuyển đổi chuỗi thành datetime object
            ngay_gio = datetime.strptime(ngay_gio_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return jsonify({'message': 'Ngày giờ không hợp lệ. Định dạng phải là YYYY-MM-DDTHH:MM:SS'}), 400

        chuyenbay = Chuyenbay( id = ma_chuyen_bay,
                              Ma_san_bay_di = ma_san_bay_di, 
                              Ma_san_bay_den = ma_san_bay_den,
                              Ma_may_bay = ma_may_bay,
                              ngay_gio = ngay_gio,
                              Thoi_gian_bay = thoi_gian_bay,
                              gia_ve = gia_ve,
                              so_ghe_hang1 = so_ghe_hang1,
                              so_ghe_hang2 = so_ghe_hang2,
                              tong_so_ghe = tongsoghe)
        
        try:
            db.session.add(chuyenbay)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': f'Lỗi không thêm được chuyến bay : {e}'}), 400
        
        for i in range(rule.Soluongsanbaytrunggian):
            if data[f'Ma_san_bay_trung_gian{i}'] != '':
                ma_san_bay_trung_gian = data[f'Ma_san_bay_trung_gian{i}']
                if ma_san_bay_trung_gian == ma_san_bay_di or ma_san_bay_trung_gian == ma_san_bay_den:
                    return jsonify({'message': 'Mã sân bay trung gian không hợp lệ'}), 400
                thoigian_dung = data[f'thoigian_dung{i}']
                
                if thoigian_dung < rule.Thoigiandungtoithieu or thoigian_dung > rule.Thoigiandungtoithieu:
                    return jsonify({'message': f'Thời gian dừng tại sân bay trung gian phải từ {rule.Thoigiandungtoithieu} đến {rule.Thoigiandungtoithieu} phút'}), 400
                
                ghichu = data[f'ghichu{i}']
                chitiet = ChiTietChuyenBay(Ma_chuyen_bay = ma_chuyen_bay, Ma_san_bay_trung_gian = ma_san_bay_trung_gian,
                                           Thoi_gian_dung = thoigian_dung, Ghi_chu = ghichu)
                db.session.add(chitiet)
                db.session.commit()
        return jsonify({'message': 'Thêm chuyến bay thành công'}), 200

    except Exception as e:
        return jsonify({'message': f'Lỗi {e}'}), 400