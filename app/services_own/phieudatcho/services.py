from pdb import runcall
from app.models import PhieuDatCho, HanhKhach, Vechuyenbay, Chuyenbay, QuyDinh, Hoadon
from library import *
from datetime import datetime, timedelta
# from extension import db
# from Chuyenbay.services import update_chuyenbay_daban, update_chuyenbay_dahuy
# from Vechuyenbay.services import update_tinhtrang_daban, update_tinhtrang_dahuy

# def add_phieu_dat_cho():
#     data = request.json
#     if data and 'Ma_hanh_khach' in data and 'Ma_ve_chuyen_bay' in data :
#         Ma_hanh_khach = data['Ma_hanh_khach']
#         Ma_ve_chuyen_bay = data['Ma_ve_chuyen_bay']
#         ngay_dat = datetime.strptime(data['ngay_dat'], '%Y-%m-%d %H:%M:%S')
        
#         hanhkhach = HanhKhach.query.get(Ma_hanh_khach)
#         vecb = Vechuyenbay.query.get(Ma_ve_chuyen_bay)
#         chuyenbay = Chuyenbay.query.get(vecb.Ma_chuyen_bay)
        
#         if not hanhkhach or not vecb:
#             return jsonify({'message': 'Ma hanh khach hoac ma ve chuyen bay khong ton tai'})
        
#         if vecb.Tinh_trang == True:
#             return jsonify({'message': 'Ve chuyen bay da ban'})

#         if ngay_dat >= chuyenbay.ngay_gio - timedelta(days = 1):  
#             return jsonify({'message': 'Ngay dat phai nho hon ngay gio khoi hanh it nhat 1 ngay'})
        
#         Tinh_trang = 0
#         ghichu = ''
#         tratien = vecb.Tien_ve
#         try:
#             phieudatcho = PhieuDatCho(Ma_hanh_khach = Ma_hanh_khach, Ma_vecb = Ma_ve_chuyen_bay, Ngay_dat = ngay_dat, Tinh_trang = Tinh_trang, Ghi_chu = ghichu, Tra_tien = tratien)
#             db.session.add(phieudatcho)
#             db.session.commit()
#             if update_tinhtrang_daban(vecb):
#                 if update_chuyenbay_daban(chuyenbay):
#                     return jsonify({'message': 'Them phieu dat cho thanh cong'})
#                 else:
#                     update_tinhtrang_dahuy(vecb)
#                     db.session.delete(phieudatcho)
#                     return jsonify({'message': 'Cap nhat chuyen bay that bai'})
#             return jsonify({'message': 'Them phieu dat cho thanh cong'})
#         except:
#             return jsonify({'message': 'Them phieu dat cho that bai'})
        
#     else:
#         return jsonify({'message': 'Thieu thong tin'})



# def Delete_or_confirm_phieu_dat_cho(phieudatcho: PhieuDatCho):
#     try:
#         vecb = Vechuyenbay.query.get(phieudatcho.Ma_vecb)
#         chuyenbay = Chuyenbay.query.get(vecb.Ma_chuyen_bay)
#         if phieudatcho.Tinh_trang == 0:
#             if update_tinhtrang_dahuy(vecb):
#                 if update_chuyenbay_dahuy(chuyenbay):
#                     db.session.delete(phieudatcho)
#                     db.session.commit()
#                     return True
#                 else:
#                     update_tinhtrang_daban(vecb)
#                     return False
#             return False
#         return False
#     except:
#         return False


def get_phieu_dat_cho(id):
    try:
        phieudatcho = PhieuDatCho.query.get(id)
        return jsonify({
            'Ma_hanh_khach': phieudatcho.Ma_hanh_khach,
            'Ma_chuyen_bay': phieudatcho.Ma_cb,
            'Ngay_dat': phieudatcho.Ngay_dat,
            'Tinh_trang': phieudatcho.Tinh_trang,
            'Vi_tri': phieudatcho.vi_tri,
            'Hang_ve': phieudatcho.hang_ve,
            'Tra_tien': phieudatcho.tra_tien
        }), 200
    except Exception as e:
        error_message = traceback.format_exc()
        return jsonify({'message': f'Loi truy cap: {error_message}'}), 400
    

def add_phieudatcho():
    try:
        rule = QuyDinh.query.first()
    except:
        return jsonify({'message': "Lỗi truy cập quy định"}), 400
    try:
        data = request.get_json()

        tmp = ['hoten', 'cmnd', 'sdt', 'gioi_tinh', 'machuyenbay', 'hangve', 'vi_tri']
        if data is None or not all(k in data for k in tmp):
            return jsonify({'message': 'Thiếu thông tin'}), 400

        hoten = data['hoten']
        cmnd = data['cmnd']
        sdt = data['sdt']
        gioi_tinh = data['gioi_tinh']
        machuyenbay = data['machuyenbay']
        hangve = data['hangve']
        vi_tri = data['vi_tri']
        
        

        ngaydat = datetime.utcnow()
        chuyenbay = Chuyenbay.query.get(machuyenbay)
        if chuyenbay is None:
            return jsonify({'message': 'Chuyến bay không tồn tại'}), 404
        
        if chuyenbay.get_ngaygio() - ngaydat < timedelta(days=1):
            return jsonify({'message': 'Chỉ cho đặt vé chậm nhất 1 ngày trước khi bay'}), 400
        
        if chuyenbay.get_sogheconlai(hangve) == 0:
            return jsonify({'message': f'Hạng ghế {hangve} đã hết chỗ'}), 400



        hanhkhach = HanhKhach.query.filter_by(cmnd = cmnd).first()
        if hanhkhach is None:
            hanhkhach= HanhKhach(Hoten = hoten, cmnd = cmnd, sdt = sdt, gioi_tinh = gioi_tinh, ngaydangky = ngaydat)
            try:
                db.session.add(hanhkhach)
                db.session.commit()
            except Exception as e:
                return jsonify({'message': f'Lỗi không xác định: {e}'}), 400

        
        if chuyenbay.set_ghedadat(hangve) == False:
            return jsonify({'message': 'Lỗi không xác định'}), 400

        if hangve == 1:
            giave = chuyenbay.get_giave() * rule.get_Phantramgia1() /100
        else:
            giave = chuyenbay.get_giave() * rule.get_Phantramgia2() /100
        tinhtrang = 0
        mahk = hanhkhach.get_mahk()
        phieudatcho = PhieuDatCho(Ma_hanh_khach = mahk, 
                                Ma_cb = machuyenbay,
                                Ngay_dat = ngaydat, 
                                Tinh_trang = tinhtrang, 
                                hang_ve = hangve, 
                                tra_tien = giave, 
                                vi_tri = vi_tri)
        db.session.add(phieudatcho)
        db.session.commit()
        return jsonify({'message': 'Đặt chỗ thành công. Vui lòng thanh toán trong 24h tới nếu không phiếu đặt chỗ sẽ bị hủy.'}), 200



    except Exception as e:
        error_message = traceback.format_exc()
        return jsonify({'message': f'Lỗi không xác định: {error_message}'}), 400
        # return jsonify({'message': ''}), 400
    

# {
#     "hoten" : "Cao Thanh Huy",
#     "cmnd": "12456759",
#     "sdt": "035264964",
#     "gioi_tinh": "nam",
#     "machuyenbay": 2,
#     "hangve": 1,
#     "vi_tri": "5.12"
# }



def Thanhtoan_phieudatcho_services():
    try:
        data = request.get_json()
        if data and 'Ma_phieu' in data:
            Ma_phieu = data['Ma_phieu']
            try:
                phieudatcho = PhieuDatCho.query.get(Ma_phieu)
            except:
                return jsonify({'message': 'Lỗi truy cập phiếu đặt chỗ'}), 400
                              
            
            vechuyenbay = Vechuyenbay()

            try:
            
                if vechuyenbay.create_ve_by_phieudat(phieudatcho) == False:
                    return jsonify({'message': f'Lỗi tạo vé chuyến bay'}), 400

                hoadon = Hoadon()
                if hoadon.Add_hoadon(vechuyenbay) == False:
                    return jsonify({'message': f'Lỗi tạo hóa đơn'}), 400
                
                if phieudatcho.set_thanhtoan() == False:
                    return jsonify({'message': f'Lỗi cập nhật phiếu đặt chỗ'}), 400  

                return jsonify({'message': 'Thanh toán thành công'}), 200
        
            except Exception as e:
                db.session.rollback()
                return jsonify({'message': f'Lỗi không xác định: {e}'}), 400
            

        return jsonify({'message': 'Nhập phiếu đặt chỗ vào'}), 400       

    except:
        error_message = traceback.format_exc()
        return jsonify({'message': f'Lỗi không xác định: {error_message}'}), 400
    
