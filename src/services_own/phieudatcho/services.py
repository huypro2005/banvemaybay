from pdb import runcall
from src.models import PhieuDatCho, HanhKhach, Vechuyenbay, Chuyenbay, QuyDinh, Hoadon
from library import *
from datetime import datetime, timedelta
from time import sleep



def get_phieu_dat_cho(id):
    try:
        phieudatcho = PhieuDatCho.query.get(id)
        hanhkhach = HanhKhach.query.get(phieudatcho.Ma_hanh_khach)
        return jsonify({
            'Ma_hanh_khach': phieudatcho.Ma_hanh_khach,
            'Hoten': hanhkhach.Hoten,
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
    rule = QuyDinh.query.first_or_404()
    if rule is None:
        return jsonify({'message': 'Lỗi truy cập quy định.'}), 500
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
        return jsonify({'message': f'Đặt chỗ thành công. Vui lòng thanh toán {phieudatcho.tra_tien}VND trong 24h tới nếu không phiếu đặt chỗ sẽ bị hủy.'}), 200



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

        if 'Ma_phieu' not in data:
            return jsonify({'message': 'Thiếu thông tin'}), 400
        
        Ma_phieu = data['Ma_phieu']

        phieudatcho = PhieuDatCho.query.get(Ma_phieu)

        if phieudatcho is None:
            return jsonify({'message': 'Lỗi truy cập phiếu đặt chỗ'}), 400
                            
        if phieudatcho.Tinh_trang == 1:
            return jsonify({'message': 'Phiếu đặt chỗ đã thanh toán rồi'}), 400
        
        if phieudatcho.Tinh_trang == 2:
            return jsonify({'message': 'Phiếu đặt chỗ đã bị hủy'}), 400

        vechuyenbay = Vechuyenbay()

        
        if vechuyenbay.create_ve_by_phieudat(phieudatcho) == False:
            return jsonify({'message': f'Lỗi tạo vé chuyến bay'}), 400

        hoadon = Hoadon()
        if hoadon.Add_hoadon(vechuyenbay) == False:
            return jsonify({'message': f'Lỗi tạo hóa đơn'}), 400
        
        if phieudatcho.set_thanhtoan() == False:
            return jsonify({'message': f'Lỗi cập nhật phiếu đặt chỗ'}), 400  
        
        data = {
            'Ma_ve': vechuyenbay.id,
            'Ma_chuyen_bay': vechuyenbay.Ma_chuyen_bay,
            'Hang_ve': vechuyenbay.hang_ve,
            'Tien_ve': vechuyenbay.Tien_ve,
            'Ma_hanh_khach': vechuyenbay.Ma_hanh_khach
        }

        return jsonify({'message': 'Thanh toán thành công', 'vecb': data,
                        'Ma_hoadon': hoadon.id}), 200
        

    except:
        error_message = traceback.format_exc()
        return jsonify({'message': f'Lỗi không xác định: {error_message}'}), 400
    
def get_ds_Phieudatcho_of_HK(mahk):
    try:
        ds = PhieuDatCho.query.filter_by(Ma_hanh_khach=mahk).all()
        data = []
        for phieudatcho in ds:
            data.append({
                'Ma_phieu': phieudatcho.id,
                'Ma_chuyen_bay': phieudatcho.Ma_cb,
                'Ngay_dat': phieudatcho.Ngay_dat,
                'Tinh_trang': phieudatcho.Tinh_trang,
                'Hang_ve': phieudatcho.hang_ve,
                'Ma_hanh_khach': phieudatcho.Ma_hanh_khach
            })
        return jsonify({'ds': data})
    except Exception as e:
        return jsonify({'message': f'Lỗi truy cập phiếu đặt chỗ: {e}'})
    



