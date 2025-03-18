from app import db
from datetime import datetime
from .Vechuyenbay import Vechuyenbay

class Hoadon(db.Model):
    __tablename__ = 'hoa_don'
    id = db.Column(db.Integer, primary_key=True)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'))
    Ma_ve_cb = db.Column(db.Integer, db.ForeignKey('ve_chuyen_bay.id'))
    Loai_hoa_don = db.Column(db.Boolean, default = False) # 0: Thanh toan , 1: Hoan tien
    Ngay_lap = db.Column(db.DateTime, default = datetime.now)
    Thanh_tien = db.Column(db.Float)
    Ghi_chu = db.Column(db.String(100), nullable = True)

    def Add_hoadon(self, vecb: Vechuyenbay):
        try:
            self.Ma_hanh_khach = vecb.Ma_hanh_khach
            self.Ma_ve_cb = vecb.id
            self.Thanh_tien = vecb.Tien_ve
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False