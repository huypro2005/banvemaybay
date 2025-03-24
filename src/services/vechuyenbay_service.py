# from app.models import Vechuyenbay, Chuyenbay, HanhKhach, QuyDinh
from src.modelss.Phieudatcho import PhieuDatCho
from src.modelss.Quydinh import QuyDinh
from src.modelss.Vechuyenbay import Vechuyenbay
from src.modelss.Chuyenbay import Chuyenbay
from src.modelss.HanhKhach import HanhKhach
from library import *
from src import db
from src.services_own.Hoadon.services import add_Hoadon
from datetime import datetime

rule = QuyDinh.query.first()

def add_ve():
    try:
        data = request.get_json()
        macb = data['Ma_cb']
        Hoten = data['Ho_ten']
        cmnd = data['cmnd']
        sdt = data['sdt']
        gioi_tinh = data['gioi_tinh']
        hang_ve = data['hang_ve']
        vitri = data['vitri']
        ma_hanh_khach =''
        giave =0
        chuyenbay = Chuyenbay.query.filter_by(id = macb).first()
        if not chuyenbay:
            return jsonify({'message': 'Mã chuyến bay không hợp lệ'}), 400
        
        if hang_ve == 'hang1':
            if chuyenbay.so_ghe_hang1 == 0:
                return jsonify({'message': 'Hết vé'}), 400
            chuyenbay.so_ghe_hang1 -= 1
            giave = chuyenbay.gia_ve * rule.Phantramgiahang1/100
        else:
            if chuyenbay.so_ghe_hang2 == 0:
                return jsonify({'message': 'Hết vé'}), 400
            chuyenbay.so_ghe_hang2 -= 1
            giave = chuyenbay.gia_ve * rule.Phantramgia2/100
        db.session.commit()

        

        hanhkhach = HanhKhach.query.filter_by(cmnd = cmnd).first()
        
        if hanhkhach:
            ma_hanh_khach = hanhkhach.id
        else:
            hanhkhach = HanhKhach(Hoten= Hoten, cmnd = cmnd, sdt = sdt, gioi_tinh = gioi_tinh)
            db.session.add(hanhkhach)
            db.session.commit()
            ma_hanh_khach = hanhkhach.id
        
        if ma_hanh_khach == '':
            return jsonify({'message': 'Lỗi'}), 400
        
        ve = Vechuyenbay(Ma_chuyen_bay = macb, Ma_hanh_khach = ma_hanh_khach, Hang_ve = hang_ve, Tinh_trang = True, vi_tri = vitri)
        db.session.add(ve)
        db.session.commit()
        if add_Hoadon(ma_hanh_khach, ve.id, 0, datetime.utcnow(), giave):
            return jsonify({'message': 'Đặt vé thành công', 'Giá vé': giave}), 200        
        return jsonify({'message': 'Lỗi'}), 400
    except:
        return jsonify({'message': 'Lỗi'}), 400
    


def add_ve_by_datcho(madatcho):
    try:
        datcho = PhieuDatCho.query.filter_by(id = madatcho).first()
        if not datcho:
            return jsonify({'message': 'Mã đặt chỗ không hợp lệ'}), 400
        if datcho.Tinh_trang == 2:
            return jsonify({'message': 'Đã hủy đặt chỗ'}), 400
        if datcho.Tinh_trang == 1:
            return jsonify({'message': 'Đã thanh toán, và nhận vé rồi'}), 400
        



    except:
        pass