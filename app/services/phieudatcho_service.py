from sqlalchemy import false
from app.modelss.Chuyenbay import Chuyenbay
from app.modelss.Phieudatcho import PhieuDatCho
from app.modelss.Quydinh import QuyDinh
from app.modelss.HanhKhach import HanhKhach
from app.modelss.Vechuyenbay import Vechuyenbay
from app.modelss.Hoadon import Hoadon
from app import db
from datetime import datetime, timedelta
from library import *

rule = QuyDinh.query.first()

def add_phieu_dat_cho():
    try:
        data = request.json()
        hoten = data['hoten']
        cmnd = data['cmnd']
        sdt = data['sdt']
        gioi_tinh = data['gioi_tinh']
        machuyenbay = data['machuyenbay']
        hangve = data['hangve']
        vi_tri = data['vi_tri']
        
        ngaydat = datetime.now()
        chuyenbay = Chuyenbay.query.get(machuyenbay)
        if chuyenbay is None:
            return jsonify({'message': 'Chuyến bay không tồn tại'}), 404
        
        if chuyenbay.get_ngaygio() - ngaydat < timedelta(days=1):
            return jsonify({'message': 'Chỉ cho đặt vé chậm nhất 1 ngày trước khi bay'}), 400
        
        if chuyenbay.get_sogheconlai(hangve) == 0:
            return jsonify({'message': f'Hạng ghế {hangve} đã hết chỗ'}), 400



        hanhkhach = HanhKhach.query.filter_by(cmnd = cmnd).first()
        if hanhkhach is None:
            hanhkhach(Hoten = hoten, cmnd = cmnd, sdt = sdt, gioi_tinh = gioi_tinh, ngaydangky = ngaydat)
            db.session.add(hanhkhach)
            db.session.commit()
        
        if chuyenbay.set_ghedadat(hangve) == False:
            return jsonify({'message': 'Lỗi không xác định'}), 400

        if hangve == 1:
            giave = chuyenbay.get_giave() * rule.get_Phantramgia1() /100
        else:
            giave = chuyenbay.get_giave() * rule.get_Phantramgia2() /100
        tinhtrang = 0
        mahk = hanhkhach.get_mahk()
        phieudatcho = PhieuDatCho(Ma_hanh_khach = mahk, Ma_cb = machuyenbay, Ngay_dat = ngaydat, Tinh_trang = tinhtrang, Hang_ve = hangve, tra_tien = giave, vi_tri = vi_tri)
        db.session.add(phieudatcho)
        db.session.commit()
        return jsonify({'message': 'Đặt chỗ thành công. Vui lòng thanh toán trong 24h tới nếu không phiếu đặt chỗ sẽ bị hủy.'}), 200



    except:
        return jsonify({'message': 'Lỗi không xác định'}), 400
    


def Thanhtoan_phieudatcho_services():
    try:
        data = request.json()
        if data['Ma_phieu'] is not None:
            phieudatcho = PhieuDatCho.query.get(data['Ma_phieu'])
            if phieudatcho.set_thanhtoan() == False:
                return jsonify({'message': 'Lỗi không xác định'}), 400            
            mahk = phieudatcho.get_mahk()
            macb = phieudatcho.get_macb()
            hangve = phieudatcho.get_hangve()
            giave = phieudatcho.get_tratien()
            vitri = phieudatcho.get_vitri()
            
            
            vechuyenbay = Vechuyenbay()
            if vechuyenbay.create_ve_by_phieudat(phieudatcho) == False:
                return jsonify({'message': 'Lỗi không xác định'}), 400

            hoadon = Hoadon()
            if hoadon.Add_hoadon(vechuyenbay) == False:
                return jsonify({'message': 'Lỗi không xác định'}), 400
            
            return jsonify({'message': 'Thanh toán thành công'}), 200

        return jsonify({'message': 'Nhập phiếu đặt chỗ vào'}), 400       

    except:
        return jsonify({'message': 'Lỗi không xác định'}), 400