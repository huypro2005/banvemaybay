from app import db
from datetime import datetime


class Chuyenbay(db.Model):
    __tablename__ = 'chuyen_bay'
    id = db.Column(db.Integer, primary_key=True, index = True)
    Ma_san_bay_di = db.Column(db.Integer, db.ForeignKey('san_bay.id'), nullable = False, index = True)     
    Ma_san_bay_den = db.Column(db.Integer, db.ForeignKey('san_bay.id'), nullable = False, index = True)
    Ma_may_bay = db.Column(db.Integer, db.ForeignKey('may_bay.id'), nullable = False)
    ngay_gio = db.Column(db.DateTime)
    Thoi_gian_bay = db.Column(db.Integer)
    gia_ve = db.Column(db.Integer)
    so_ghe_hang1 = db.Column(db.Integer)
    so_ghe_hang2 = db.Column(db.Integer)
    tong_so_ghe = db.Column(db.Integer)

    def __repr__(self):
        return str(self.Ma_san_bay_di) + ' - ' + str(self.Ma_san_bay_den)
    

    def get_sogheconlai(self, id):
        if id == 1:
            return self.so_ghe_hang1
        else:
            return self.so_ghe_hang2

    def get_giave(self):
        return self.gia_ve
    
    def get_sanbayden(self):
        return self.Ma_san_bay_den
    
    def get_sanbaydi(self):
        return self.Ma_san_bay_di

    def get_ngaygio(self):
        return self.ngay_gio
    

    def set_ghedadat(self, id):
        try:
            if id == 1:
                self.so_ghe_hang1 -= 1
            else:
                self.so_ghe_hang2 -= 1
            db.session.commit()
            return True
        except:
            return False
        
    