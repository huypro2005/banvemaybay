from app.modelss.Chuyenbay import Chuyenbay
from datetime import datetime, timedelta, time
from app import db


def get_danhsachchuyenbay_trongkhoangngay(date1, date2):
    try:
        start_datetime = datetime.combine(date1, time.min)
        end_datetime = datetime.combine(date2, time.max)
        ds = Chuyenbay.query.filter(Chuyenbay.ngay_gio >= start_datetime, Chuyenbay.ngay_gio <= end_datetime).all()
        return ds
    except:
        return None
    

def get_danhsachchuyenbay_trongngay(date0):
    try:
        start_datetime = datetime.combine(date0, time.min)
        end_datetime = datetime.combine(date0, time.max)
        ds= Chuyenbay.query.filter(Chuyenbay.ngay_gio >= start_datetime, Chuyenbay.ngay_gio <= end_datetime).all()
        return ds
    except:
        return None