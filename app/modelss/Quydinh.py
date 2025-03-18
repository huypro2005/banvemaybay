from app import db
from datetime import datetime

class QuyDinh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Soluongsanbay = db.Column(db.Integer, default = 10)
    Thoigianbaytoithieu = db.Column(db.Integer, default = 30)
    Soluongsanbaytrunggian = db.Column(db.Integer, default = 2)
    Thoigiandungtoithieu = db.Column(db.Integer, default = 10)
    Thoigiandungtoida = db.Column(db.Integer, default = 20)
    Phantramgia1 = db.Column(db.Float, default = 105)
    Phantramgia2 = db.Column(db.Float, default = 100)
    # Soluonghangve = db.Column(db.Integer, default = 2)


    def get_Soluongsanbaytoida(self):
        return self.Soluongsanbay
    
    def get_Thoigianbaytoithieu(self):
        return self.Thoigianbaytoithieu
    
    def get_Soluongsanbaytrunggian(self):
        return self.Soluongsanbaytrunggian
    
    def get_Thoigiandungtoithieu(self):
        return self.Thoigiandungtoithieu
    
    def get_Thoigiandungtoida(self):
        return self.Thoigiandungtoida
    
    def get_Phantramgia1(self):
        return self.Phantramgia1
    
    def get_Phantramgia2(self):
        return self.Phantramgia2

    