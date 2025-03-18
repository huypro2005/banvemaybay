from app.models import HanhKhach
from library import *
# from extension import db

def add_hanh_khach():
    data = request.json
    if data and 'Hoten' in data and 'cmnd' in data and 'sdt' in data:
        Hoten = data['Hoten']
        cmnd = data['cmnd']
        sdt = data['sdt']
        gioi_tinh = data.get('gioi_tinh', '')
        dia_chi = data.get('dia_chi', '')
        # ngaydangky = datetime.utcnow()
        try: 
            hanh_khach = HanhKhach(Hoten = Hoten, cmnd = cmnd, sdt = sdt, gioi_tinh = gioi_tinh, dia_chi = dia_chi)
            db.session.add(hanh_khach)
            db.session.commit()
            return jsonify({'message': 'Hanh khach da duoc them'})
        except Exception as e:
            return jsonify({'message': f'Error: {e}'})
    return jsonify({'message': 'Thieu thong tin'})

def get_hanh_khach(id):
    hanhkhach = HanhKhach.query.get(id)
    if hanhkhach:
        return jsonify({'Hoten': hanhkhach.Hoten, 'cmnd': hanhkhach.cmnd, 'sdt': hanhkhach.sdt, 'gioi_tinh': hanhkhach.gioi_tinh, 'dia_chi': hanhkhach.dia_chi})
    return jsonify({'message': 'Khong tim thay hanh khach'})


def add_hk(hoten, cmnd, sdt, gioitinh, ngaydangky):
    try:
        hanhkhach = HanhKhach(Hoten = hoten, cmnd = cmnd, sdt = sdt, gioi_tinh= gioitinh, ngaydangky = ngaydangky)

        db.session.add(hanhkhach)
        db.session.commit()
        return True
    except:
        return False