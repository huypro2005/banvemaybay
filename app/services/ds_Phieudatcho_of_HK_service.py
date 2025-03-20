from tkinter import N
from app.modelss.Phieudatcho import PhieuDatCho


def get_ds_Phieudatcho_of_HK(mahk):
    try:
        ds = PhieuDatCho.query.filter_by(Ma_hanh_khach=mahk).all()
        return ds
    except:
        return None
    
