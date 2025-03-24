from sqlalchemy import false, true
from src import db
from .Phieudatcho import PhieuDatCho
from datetime import datetime


class Vechuyenbay(db.Model):
    __tablename__ = 've_chuyen_bay'
    id = db.Column(db.Integer, primary_key=True, index = True)
    Ma_chuyen_bay = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'), nullable = False, index=True)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'), default = None, index= True)
    hang_ve = db.Column(db.Integer)
    Tien_ve = db.Column(db.Float)
    Tinh_trang = db.Column(db.Boolean, default = False) # 0: Da dat + thanh toan, 1: Da Huy
    vi_tri = db.Column(db.String(20))



    def __repr__(self):
        return f"{self.Ma_chuyen_bay} - {self.hang_ve}"  # Sửa cách nối chuỗi


    def create_ve(self, Ma_chuyen_bay, hang_ve, Tien_ve, vi_tri, Ma_hanh_khach):
        try:
            self.Ma_chuyen_bay = Ma_chuyen_bay
            self.hang_ve = hang_ve
            self.Tien_ve = Tien_ve
            self.vi_tri = vi_tri
            self.Ma_hanh_khach = Ma_hanh_khach
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        

    def create_ve_by_phieudat(self, phieudat: PhieuDatCho):
        try:
            self.Ma_chuyen_bay = phieudat.Ma_cb
            self.hang_ve = phieudat.hang_ve
            self.Tien_ve = phieudat.tra_tien
            self.vi_tri = phieudat.vi_tri
            self.Ma_hanh_khach = phieudat.Ma_hanh_khach
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False