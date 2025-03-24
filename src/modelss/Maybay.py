from src import db
from datetime import datetime

class Maybay(db.Model):
    __tablename__ = 'may_bay'
    id = db.Column(db.Integer, primary_key = True)
    ten_may_bay = db.Column(db.String(80), unique = True)

    def __repr__(self):
        return self.ten_may_bay
    
    def get_ten_maybay(self):
        return self.ten_may_bay