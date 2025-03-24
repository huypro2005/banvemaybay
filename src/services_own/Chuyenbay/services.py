import re

from sqlalchemy import exists
from src.models import Chuyenbay, Sanbay, QuyDinh, ChiTietChuyenBay
from src import db
from library import *
from datetime import datetime
# from extension import db



def add_chuyen_bay():
    data = request.json
    if data and 'Ma_san_bay_di' in data and 'Ma_san_bay_den' in data and 'ngay_gio' in data and 'Thoi_gian_bay' in data and 'gia_ve' in data and 'so_ghe_hang1' in data and 'so_ghe_hang2' in data :
        Ma_san_bay_di = data['Ma_san_bay_di']
        Ma_san_bay_den = data['Ma_san_bay_den']
        ngay_gio = data['ngay_gio']
        Thoi_gian_bay = data['Thoi_gian_bay']
        gia_ve = data['gia_ve']
        so_ghe_hang1 = data['so_ghe_hang1']
        so_ghe_hang2 = data['so_ghe_hang2']
        if Sanbay.query.get(Ma_san_bay_di) is None or Sanbay.query.get(Ma_san_bay_den) is None:
            return jsonify({'message': 'Ma san bay khong ton tai'})
        
        if Thoi_gian_bay < 30:  
            return jsonify({'message': f'Thoi gian bay phai lon hon {30} phut'})

        try: 
            chuyen_bay = Chuyenbay(Ma_san_bay_di = Ma_san_bay_di, Ma_san_bay_den = Ma_san_bay_den, ngay_gio = ngay_gio, Thoi_gian_bay = Thoi_gian_bay, gia_ve = gia_ve, so_ghe_hang1 = so_ghe_hang1, so_ghe_hang2 = so_ghe_hang2)
            db.session.add(chuyen_bay)
            db.session.commit()
            return jsonify({'message': 'Chuyen bay da duoc them'})
        except Exception as e:
            return jsonify({'message': f'Error: {e}'})
    return jsonify({'message': 'Thieu thong tin'})


def update_chuyenbay_daban(chuyenbay : Chuyenbay, hangve):
    try:
        if hangve == 1:
            chuyenbay.so_ghe_hang1 -= 1
        else:
            chuyenbay.so_ghe_hang2 -= 1
        db.sessio.commit()
        return True
    except:
        return False


def update_chuyenbay_dahuy(chuyenbay : Chuyenbay, hangve):
    try:
        if hangve == 1:
            chuyenbay.so_ghe_hang1 +=1
        else:
            chuyenbay.so_ghe_hang2 +=1
        db.session.commit()
        return True
    except:
        return False


def get_chuyen_bay(id):
    chuyenbay = Chuyenbay.query.get(id)
    if chuyenbay:   
        return jsonify({'Ma_san_bay_di': chuyenbay.Ma_san_bay_di, 'Ma_san_bay_den': chuyenbay.Ma_san_bay_den, 'ngay_gio': chuyenbay.ngay_gio, 'Thoi_gian_bay': chuyenbay.Thoi_gian_bay, 'gia_ve': chuyenbay.gia_ve, 'so_ghe_hang1': chuyenbay.so_ghe_hang1, 'so_ghe_hang2': chuyenbay.so_ghe_hang2, 'so_ghe_trong': chuyenbay.so_ghe_trong})
    return jsonify({'message': 'Khong tim thay chuyen bay'})


def get_ngay_gio(chuyenbay: Chuyenbay):
    return chuyenbay.ngay_gio



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
            with db.session.begin():
                db.session.add(chuyenbay)
                # db.session.commit()

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
                        # db.session.commit()
                db.session.commit()
                return jsonify({'message': 'Thêm chuyến bay thành công'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Lỗi: {e}'})

    except Exception as e:
        return jsonify({'message': f'Lỗi {e}'}), 400



# {
#     "Ma_chuyen_bay": 6,
#     "Ma_san_bay_di": 1,
#     "Ma_san_bay_den": 2,
#     "Ma_may_bay": 1,
#     "gia_ve": 500000,
#     "ngay_gio": "2024-04-25T10:30:00",
#     "thoi_gian_bay": 30,
#     "so_ghe_hang1": 15,
#     "so_ghe_hang2": 20,
#     "Ma_san_bay_trung_gian0": "",
#     "thoigian_dung0": "",
#     "ghichu0": "",
#     "Ma_san_bay_trung_gian1": "",
#     "thoigian_dung1": "",
#     "ghichu1": ""
# }




def get_ds_chuyenbay_by_days_diadiem():
    try:
        data = request.get_json()
        tmp = ['sanbayden', 'sanbaydi', 'tungay', 'denngay']
        if data is None or not all(k in data for k in tmp):
            return jsonify({'message': 'Thiếu thông tin'}), 400

        
        sanbaydi = data.get('sanbaydi')
        sanbayden = data.get('sanbayden')
        tungay = data.get('tungay')
        denngay = data.get('denngay')
        if sanbaydi == sanbayden:
            return jsonify({'message': 'Mã sân bay đi và đến không được trùng'}), 400
        
        if tungay > denngay:
            return jsonify({'message': 'Ngày bắt đầu không được lớn hơn ngày kết thúc'}), 400
        
        if tungay < datetime.now():
            return jsonify({'message': 'Ngày bắt đầu không được nhỏ hơn ngày hiện tại'}), 400
        
        ds = Chuyenbay.query.filter(Ma_san_bay_di == sanbaydi, 
                                    Ma_san_bay_den == sanbayden, 
                                    ngay_gio >= tungay, 
                                    ngay_gio <= denngay).all() 
        data = []
        for i in ds:
            data.append({
                'id': i.id,
                'Ma_san_bay_di': i.Ma_san_bay_di,
                'Ma_san_bay_den': i.Ma_san_bay_den,
                'ngay_gio': i.ngay_gio,
                'Thoi_gian_bay': i.Thoi_gian_bay,
                'gia_ve': i.gia_ve,
                'so_ghe_hang1': i.so_ghe_hang1,
                'so_ghe_hang2': i.so_ghe_hang2
            })
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'message': f'Lỗi {e}'}), 400
    