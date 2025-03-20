from app.models import Vechuyenbay, Chuyenbay, HanhKhach
from library import *
# from extension import db




def  add_ve_chuyen_bay():
    data  = request.json
    if data and 'ma_chuyen_bay' in data and 'hang_ve' in data :
        Ma_chuyen_bay = data['ma_chuyen_bay']
        hang_ve = data['hang_ve']
        # ma_hanh_khach = data['ma_hanh_khach']
        try:
            chuyenbay = Chuyenbay.query.get(Ma_chuyen_bay)
            
            # if HanhKhach.query.get(ma_hanh_khach) is None:
            #     return jsonify({'message': 'Khong tim thay hanh khach'}), 404
            
            if hang_ve not in [1, 2]:
                return jsonify({'message': 'Hang ve khong hop le'}), 400
            elif hang_ve == 1:
                tien_ve = chuyenbay.giave *1.05
            else:
                tien_ve = chuyenbay.gia_ve 

            try: 
                
                ve_chuyen_bay = Vechuyenbay(Ma_chuyen_bay = Ma_chuyen_bay, hang_ve = hang_ve, Tien_ve = tien_ve)
                db.session.add(ve_chuyen_bay)
                db.session.commit()
                return jsonify({'message': 'Ve chuyen bay da duoc them'}), 201
            except:
                return jsonify({'message': 'Co loi xay ra'}), 500
        except:
            return jsonify({'message': 'Khong tim thay chuyen bay'}), 404
        
    return jsonify({'message': 'Thieu thong tin'}), 400

def update_tinhtrang_daban(vecb : Vechuyenbay, ma_hanh_khach):
    try:
        if HanhKhach.query.get(ma_hanh_khach) is None:
            return False
        vecb.Tinh_trang = True
        vecb.Ma_hanh_khach = ma_hanh_khach
        db.session.commit()
        return True
    except:
        return False


def update_tinhtrang_dahuy(vecb : Vechuyenbay):
    try:
        vecb.Tinh_trang = False
        vecb.Ma_hanh_khach = None
        db.session.commit()
        return True
    except:
        return False

def get_ve_chuyen_bay(id):
    ve_chuyen_bay = Vechuyenbay.query.get(id)
    if ve_chuyen_bay:
        return jsonify({'Ma_chuyen_bay': ve_chuyen_bay.Ma_chuyen_bay, 'hang_ve': ve_chuyen_bay.hang_ve, 'vi_tri': ve_chuyen_bay.vi_tri, 'Ma_hanh_khach': ve_chuyen_bay.Ma_hanh_khach}), 200
    return jsonify({'message': 'Khong tim thay ve chuyen bay'}), 404
# Compare this snippet from banvemaybay/app/check/Vechuyenbay/services.py:


def add_ve_cb(Ma_chuyen_bay, hang_ve, Tien_ve, Tinh_trang):
    try:
        ve_cb = Vechuyenbay(Ma_chuyen_bay = Ma_chuyen_bay, hang_ve = hang_ve, Tien_ve = Tien_ve, Tinh_trang = Tinh_trang)
        db.session.add(ve_cb)
        db.session.commit()
        return True
    except:
        return False
    
