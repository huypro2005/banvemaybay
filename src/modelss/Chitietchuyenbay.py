from src import db
from datetime import datetime

class ChiTietChuyenBay(db.Model):
    table_name = 'chi_tiet_chuyen_bay'
    id = db.Column(db.Integer, primary_key=True)
    Ma_chuyen_bay = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'))
    Ma_san_bay_trung_gian = db.Column(db.Integer, db.ForeignKey('san_bay.id'))
    Thoi_gian_dung = db.Column(db.Integer)
    Ghi_chu = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.Ma_chuyen_bay} - {self.Ma_san_bay_trung_gian}'
    