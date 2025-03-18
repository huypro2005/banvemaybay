from library import *
# from extension import db
from app.models import Hoadon, Vechuyenbay, Sanbay, Maybay, Chuyenbay


def add_Hoadon(mahk, mavcb, Loaihoadon, ngaylap, thanhtien, ghichu: None):
    try:
        hoadon = Hoadon(Ma_hanh_khach = mahk, Ma_ve_cb = mavcb, Loai_hoa_don = Loaihoadon, Ngay_lap = ngaylap, Thanh_tien = thanhtien, Ghi_chu = ghichu)
        db.session.add(hoadon)
        db.session.commit()
        return True
    except:
        return False