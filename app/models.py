from sqlalchemy import true
from app import db
from datetime import datetime
# QĐ1: Có 10 sân bay. Thời gian bay tối thiểu là 30 phút. Có tối đa 2 sân bay trung gian với thời gian dừng từ 10 đến 20 phút.
# QĐ2: Chỉ bán vé khi còn chỗ. Có 2 hạng vé (1, 2). Vé hạng 1 bằng 105% của đơn giá, vé hạng 2 bằng với đơn giá, mỗi chuyến bay có một giá vé riêng.
# QĐ3: Chỉ cho đặt vé chậm nhất 1 ngày trước khi khởi hành. Vào ngày khởi hành tất cả các phiếu đặt sẽ bị hủy.
# QĐ6: Người dùng có thể thay đổi các qui định như sau: 
#       + QĐ1: Thay đổi số lượng sân bay, thời gian bay tối thiểu, số sân bay trung gian tối đa, thời gian dừng tối thiểu/ tối đa tại các sân bay trung gian.
#       + QĐ2: Thay đổi số lượng các hạng vé.
#       + QĐ3: Thay đổi thời gian chậm nhất khi đặt vé, thời gian hủy đặt vé.


class HanhKhach(db.Model):
    __tablename__ = 'hanh_khach'
    id = db.Column(db.Integer, primary_key=True, index = True)
    Hoten = db.Column(db.String(50), nullable = False, index = True)
    cmnd = db.Column(db.String(30), nullable = False, unique = True)
    sdt = db.Column(db.String(15), nullable = False, unique = True)
    gioi_tinh = db.Column(db.String(10))
    ngaydangky = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return self.Hoten
    
    def get_mahk(self):
        return self.id
    
    




class Sanbay(db.Model):
    __tablename__ = 'san_bay'
    id = db.Column(db.Integer, primary_key=True, index = True)
    ten_san_bay = db.Column(db.String(50), nullable = False, index = True, unique= True)

    def __repr__(self):
        return self.ten_san_bay

    # Has max 10 flights
    # def Rule1(self):

class Maybay(db.Model):
    __tablename__ = 'may_bay'
    id = db.Column(db.Integer, primary_key = True)
    ten_may_bay = db.Column(db.String(80), unique = True)

    def __repr__(self):
        return self.ten_may_bay
    
        



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
    

    def get_sogheconlai(self, hang_ve):
        if hang_ve == 1:
            return self.so_ghe_hang1
        else:
            return self.so_ghe_hang2
        
    def set_ghedadat(self, hang_ve):
        try:
            if hang_ve == 1:
                self.so_ghe_hang1 -= 1
            else:
                self.so_ghe_hang2 -= 1
            db.session.commit()
            return True
        except:
            return False
        
    def get_ngaygio(self):
        return self.ngay_gio
    
    def get_giave(self):
        return self.gia_ve

    # def Rule1_Thoigianbay(self):
    #     if self.Thoi_gian_bay < 30:
    #         return False
    #     return True



class PhieuDatCho(db.Model):
    __tablename__ = 'phieu_dat_cho'
    id = db.Column(db.Integer, primary_key=True)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'))
    Ma_cb = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'))
    Ngay_dat = db.Column(db.DateTime, default = datetime.now, index = True)
    Tinh_trang = db.Column(db.Integer) # 0: Da dat ve chua thanh toan, 1: Da thanh toan da nhan ve, 2: Da huy ve
    vi_tri = db.Column(db.String(20))
    # Ghi_chu = db.Column(db.String(100)) 
    hang_ve = db.Column(db.Integer)
    tra_tien = db.Column(db.Float)

    def __repr__(self):
        return f'{self.Ma_hanh_khach} - {self.Ma_vecb} - {self.Ma_chuyen_bay} - {self.Ngay_dat} - {self.Tinh_trang} - {self.Ghi_chu} - {self.tra_tien}'
    
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
        return self.vi_tri




class Vechuyenbay(db.Model):
    __tablename__ = 've_chuyen_bay'
    id = db.Column(db.Integer, primary_key=True, index = True)
    Ma_chuyen_bay = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'), nullable = False)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'), nullable = True, default = None)
    hang_ve = db.Column(db.Integer)
    Tien_ve = db.Column(db.Float)
    Tinh_trang = db.Column(db.Boolean, default = False) # 0: chua dat, 1: da dat
    vi_tri = db.Column(db.String(20))



    __table_args__ = (db.UniqueConstraint('Ma_chuyen_bay', 'vi_tri', name ='uq_machuyenbay_vitri'),) # Đảm bảo không có 2 vé giống nhau trong 1 chuyến bay

    def __repr__(self):
        return f"{self.Ma_chuyen_bay} - {self.hang_ve} - {self.vi_tri}"  # Sửa cách nối chuỗi

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
    
    # def get_ve_chuyen_bay(self):
        


class ChiTietChuyenBay(db.Model):
    table_name = 'chi_tiet_chuyen_bay'
    id = db.Column(db.Integer, primary_key=True)
    Ma_chuyen_bay = db.Column(db.Integer, db.ForeignKey('chuyen_bay.id'))
    Ma_san_bay_trung_gian = db.Column(db.Integer, db.ForeignKey('san_bay.id'))
    Thoi_gian_dung = db.Column(db.Integer)
    Ghi_chu = db.Column(db.String(100))

    def __repr__(self):
        return f'{self.Ma_chuyen_bay} - {self.Ma_san_bay_trung_gian}'
    
    # def Rule1_Sanbaytrunggian(self):
    #     if self.Thoi_gian_dung < 10 or self.Thoi_gian_dung > 20:
    #         return False
    #     return True
    

class Nhanvien(db.Model):
    __tablename__ = 'nhan_vien'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(50), unique = True)
    password = db.Column(db.Text)
    email = db.Column(db.String(120), unique = True)
    pos = db.Column(db.Integer)

    def __repr__(self):
        return self.name
    
    def create_user(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = password 
        self.email = email
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False



class Hoadon(db.Model):
    __tablename__ = 'hoa_don'
    id = db.Column(db.Integer, primary_key=True)
    Ma_hanh_khach = db.Column(db.Integer, db.ForeignKey('hanh_khach.id'))
    Ma_ve_cb = db.Column(db.Integer, db.ForeignKey('ve_chuyen_bay.id'))
    Ma_nhan_vien = db.Column(db.Integer, db.ForeignKey('nhan_vien.id'), nullable = True)
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



class doanhThuThang(db.Model):
    __tablename__ = 'doanh_thu_thang'
    id = db.Column(db.Integer, primary_key=True)
    Tong_doanh_thu = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    def __repr__(self):
        return f'{self.Tong_doanh_thu} - {self.month} - {self.year}'
    
class doanhThuNam(db.Model):
    __tablename__ = "doanh_thu_nam"
    id = db.Column(db.Integer, primary_key = True)
    Tong_doanh_thu = db.Column(db.Float)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.Tong_doanh_thu} - {self.year}'

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

        
    def __repr__(self):
        # return f'{self.Soluongsanbay} - {self.Thoigianbaytoithieu} - {self.Soluongsanbaytrunggian} - {self.Thoigiandungtoithieu} - {self.Thoigiandungtoida} - {self.Phantramgia1} - {self.Phantramgia2}'
        return f'So luong san bay: {self.Soluongsanbay} - Thoi gian bay toi thieu: {self.Thoigianbaytoithieu} - So luong san bay trung gian: {self.Soluongsanbaytrunggian} - Thoi gian dung toi thieu: {self.Thoigiandungtoithieu} - Thoi gian dung toi da: {self.Thoigiandungtoida} - Phan tram gia ve hang 1: {self.Phantramgia1} - Phan tram gia ve hang 2: {self.Phantramgia2}'

    def get_Phantramgia1(self):
        return self.Phantramgia1
    
    def get_Phantramgia2(self):
        return self.Phantramgia2
