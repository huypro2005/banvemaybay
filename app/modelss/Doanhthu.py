from app import db
from datetime import datetime


class doanhThu(db.Model):
    __tablename__ = 'doanh_thu'
    id = db.Column(db.Integer, primary_key=True)
    Tong_doanh_thu = db.Column(db.Float)
    ThoiGian = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return f'{self.Tong_doanh_thu} - {self.ThoiGian}'
    