import json
from app import db
from datetime import datetime
from flask import jsonify


class PhieuDatCho(db.Model):
    __tablename__ = 'phieu_dat_cho'
    id = db.Column(db.Integer, primary_key=True)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'))
    Ma_cb = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'))
    Ngay_dat = db.Column(db.DateTime, default = datetime.now, index = True)
    Tinh_trang = db.Column(db.Integer) # 0: Da dat ve chua thanh toan, 1: Da thanh toan da nhan ve, 2: Da huy ve
    hang_ve = db.Column(db.Integer)
    vi_tri = db.Column(db.String(20))
    tra_tien = db.Column(db.Float)

    def __repr__(self):
        return f'{self.Ma_hanh_khach} - {self.Ma_vecb} - {self.Ma_chuyen_bay} - {self.Ngay_dat} - {self.Tinh_trang} - {self.Ghi_chu} - {self.tra_tien}'
    

    def get_tinhtrang(self):
        if self.Tinh_trang == 0:
            return jsonify({"message": 'Đã đặt vé chưa thanh toán', 'tinhtrang' : 0})
        elif self.Tinh_trang == 1:
            return jsonify({"message": 'Đã thanh toán đã nhận vé', 'tinhtrang' : 1})
        else:
            return jsonify({"message": 'Đã hủy vé', 'tinhtrang' : 2})
        
    def set_huyve(self):
        try:
            self.Tinh_trang = 2
            db.session.commit()
            return True
        except:
            return False
        
    def set_thanhtoan(self):
        try:
            self.Tinh_trang = 1
            db.session.commit()
            return True
        except:
            return False
        
    def get_mahk(self):
        return self.Ma_hanh_khach
    
    def get_macb(self):
        return self.Ma_cb
    
    def get_hangve(self):
        return self.hang_ve
    
    def get_tratien(self):
        return self.tra_tien
    
    def get_vitri(self):
        return self.vitri