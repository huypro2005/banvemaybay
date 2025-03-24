from src import db
from datetime import datetime


class Sanbay(db.Model):
    __tablename__ = 'san_bay'
    id = db.Column(db.Integer, primary_key=True, index = True)
    ten_san_bay = db.Column(db.String(50), nullable = False, index = True, unique= True)

    def __repr__(self):
        return self.ten_san_bay
