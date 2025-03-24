from flask import session
from app.models import Hoadon, Vechuyenbay, Chuyenbay, HanhKhach, QuyDinh
from library import *
from datetime import datetime
# from extension import db




# def  add_ve_chuyen_bay():
#     data  = request.json
#     if data and 'ma_chuyen_bay' in data and 'hang_ve' in data :
#         Ma_chuyen_bay = data['ma_chuyen_bay']
#         hang_ve = data['hang_ve']
#         # ma_hanh_khach = data['ma_hanh_khach']
#         try:
#             chuyenbay = Chuyenbay.query.get(Ma_chuyen_bay)
            
#             # if HanhKhach.query.get(ma_hanh_khach) is None:
#             #     return jsonify({'message': 'Khong tim thay hanh khach'}), 404
            
#             if hang_ve not in [1, 2]:
#                 return jsonify({'message': 'Hang ve khong hop le'}), 400
#             elif hang_ve == 1:
#                 tien_ve = chuyenbay.giave *1.05
#             else:
#                 tien_ve = chuyenbay.gia_ve 

#             try: 
                
#                 ve_chuyen_bay = Vechuyenbay(Ma_chuyen_bay = Ma_chuyen_bay, hang_ve = hang_ve, Tien_ve = tien_ve)
#                 db.session.add(ve_chuyen_bay)
#                 db.session.commit()
#                 return jsonify({'message': 'Ve chuyen bay da duoc them'}), 201
#             except:
#                 return jsonify({'message': 'Co loi xay ra'}), 500
#         except:
#             return jsonify({'message': 'Khong tim thay chuyen bay'}), 404
        
#     return jsonify({'message': 'Thieu thong tin'}), 400



def get_ve_chuyen_bay(id):
    ve_chuyen_bay = Vechuyenbay.query.get(id)
    if ve_chuyen_bay:
        return jsonify({'Ma_chuyen_bay': ve_chuyen_bay.Ma_chuyen_bay, 'hang_ve': ve_chuyen_bay.hang_ve, 'vi_tri': ve_chuyen_bay.vi_tri, 'Ma_hanh_khach': ve_chuyen_bay.Ma_hanh_khach}), 200
    return jsonify({'message': 'Khong tim thay ve chuyen bay'}), 404
# Compare this snippet from banvemaybay/app/check/Vechuyenbay/services.py:




def add_ve():
    try:
        rule = QuyDinh.query.first()
    except:
        return jsonify({'message': 'Lỗi truy cập quy định.'})
    try:
        data = request.get_json()
        macb = data['Ma_cb']
        Hoten = data['Ho_ten']
        cmnd = data['cmnd']
        sdt = data['sdt']
        gioi_tinh = data['gioi_tinh']
        hang_ve = data['hang_ve']
        vitri = data['vitri']
        ma_hanh_khach =None
        if hang_ve not in [1, 2]:
            return jsonify({'message': 'Hạng vé không hợp lệ'}), 400
        giave =0
        chuyenbay = Chuyenbay.query.filter_by(id = macb).first()
        if not chuyenbay:
            return jsonify({'message': 'Mã chuyến bay không hợp lệ'}), 400
        
        if hang_ve == 1:
            if chuyenbay.get_sogheconlai(1) == 0:
                return jsonify({'message': 'Hết vé'}), 400
            # chuyenbay.so_ghe_hang1 -= 1
            giave = chuyenbay.gia_ve * rule.Phantramgiahang1/100
        else:
            if chuyenbay.get_sogheconlai(2) == 0:
                return jsonify({'message': 'Hết vé'}), 400
            # chuyenbay.so_ghe_hang2 -= 1
            giave = chuyenbay.gia_ve * rule.Phantramgia2/100
        # db.session.commit()

        

        hanhkhach = HanhKhach.query.filter_by(cmnd = cmnd).first()
        
        if hanhkhach:
            ma_hanh_khach = hanhkhach.id
        else:
            hanhkhach = HanhKhach(Hoten= Hoten, cmnd = cmnd, sdt = sdt, gioi_tinh = gioi_tinh)
            try:
                db.session.add(hanhkhach)
                db.session.commit()
            except:
                return jsonify({'message': 'Thêm hành khách thất bại'})
            ma_hanh_khach = hanhkhach.id
        
        if ma_hanh_khach is None:
            return jsonify({'message': 'Lỗi tạo hành khách'}), 400
        
        
        ve = Vechuyenbay(Ma_chuyen_bay = macb, Ma_hanh_khach = ma_hanh_khach, hang_ve = hang_ve, Tinh_trang = True, vi_tri = vitri, Tien_ve = giave)
        try:
            db.session.add(ve)
            db.session.commit()
        except Exception as e:
            return jsonify({'message': f'đặt vé fail: {e}'})
        
        if chuyenbay.set_ghedadat(hang_ve) == False:
            db.session.rollback()
            return jsonify({'message': 'Truy cập chuyến bay thất bại'})


        hoadon = Hoadon()

        if hoadon.Add_hoadon(ve):
            return jsonify({'message': 'Đặt vé thành công', 'Giá vé': giave}), 200        
       

        return jsonify({'message': 'Lỗi tạo hóa đơn'}), 400
    except Exception as e:
        return jsonify({'message': f'Lỗi: {e}'}), 400
    
