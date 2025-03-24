from src import db
from datetime import datetime



class HanhKhach(db.Model):
    __tablename__ = 'hanh_khach'
    id = db.Column(db.Integer, primary_key=True, index = True)
    Hoten = db.Column(db.String(50), nullable = False, index = True)
    cmnd = db.Column(db.String(30), nullable = False, unique = True)
    sdt = db.Column(db.String(15), nullable = False, unique = True)
    gioi_tinh = db.Column(db.String(10))
    # dia_chi = db.Column(db.String(100))
    ngaydangky = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return self.Hoten


    def get_mahk(self):
        return self.id
    
    def get_hoten(self):
        return self.Hoten
    
    def get_cmnd(self):
        return self.cmnd
    
    def get_sdt(self):
        return self.sdt
    
    