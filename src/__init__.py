from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .extension import db, migrate
from .models import *
from .services_own.SanBay.controller import SANBAY
from .services_own.Maybay.controller import MAYBAY
from .services_own.Hanhkhach.controller import HANHKHACH
from .services_own.Chuyenbay.controller import chuyenbay_bp
from .services_own.phieudatcho.controller import phieudatcho_bp
from .services_own.Vechuyenbay.controller import vechuyenbay_bp
from .services_own.Quydinh.controller import QUYDINH
from datetime import datetime, timedelta
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import os

def auto_cancel_expired_bookings(app):
    with app.app_context():
        # while True:
            try:
                ds = PhieuDatCho.query.filter(
                    PhieuDatCho.Tinh_trang == 0,
                    PhieuDatCho.Ngay_dat + timedelta(days=1) < datetime.utcnow()
                ).all()
                for phieudatcho in ds:
                    phieudatcho.Tinh_trang = 2
                    db.session.commit()
                print('Da huy phieu dat cho qua han')
            except Exception as e:
                print(f'Lỗi: {e}')  

            # sleep(3)

def auto_cancel_bookings_when_flight(app):
    with app.app_context():
        try:    
            ds = Chuyenbay.query.filter(
                Chuyenbay.ngay_gio <= datetime.utcnow()
            ).all()
            bookings = []
            for chuyen in ds:
                bookings = PhieuDatCho.query.filter(
                    PhieuDatCho.Ma_cb == chuyen.id,
                    PhieuDatCho.Tinh_trang != 2
                ).all()

                for booking in bookings:
                    booking.Tinh_trang = 2
                db.session.commit()
                print(f'Hủy các phiếu đặt khi chuyến bay {chuyen.id} cất cánh')
            
            

        except Exception as e:
            print(f'Lỗi: {e}')

def init_scheduler_paying(app):
    
    scheduler = BackgroundScheduler()

    # scheduler.add_job(
    #     func=auto_cancel_expired_bookings,
    #     args=[app],
    #     trigger= 'interval',
    #     seconds = 8
    # )

    scheduler.add_job(
        func=auto_cancel_expired_bookings,
        args=[app],
        trigger= 'interval',
        seconds = 60,
        id='auto_cancel_job_paying'
    )
    scheduler.start()
    return scheduler

def init_scheduler_flight(app):
    scheduler = BackgroundScheduler()

    # scheduler.add_job(
    #     func=auto_cancel_bookings_when_flight,
    #     args=[app],
    #     trigger= 'interval',
    #     seconds =3
    # )

    scheduler.add_job(
        func=auto_cancel_bookings_when_flight,
        args=[app],
        minutes = 30,
        trigger= 'interval',
        id= 'auto_cancel_job_flight'
    )
    scheduler.start()
    return scheduler

def init_thread(app):
    thread = Thread(target=auto_cancel_expired_bookings, args=[app])

    thread.start()


def create_db(app):
    if not os.path.exists('/database/airport.db'):
        with app.app_context():
            db.create_all()
        print('create db!')

def create_app(config_file = 'config.py'):
    app= Flask(__name__)

    app.config.from_pyfile(config_file)
    
    print('config success')
    db.init_app(app)
    migrate.init_app(app, db)
    create_db(app)
    app.register_blueprint(chuyenbay_bp)
    app.register_blueprint(SANBAY)
    app.register_blueprint(MAYBAY)
    app.register_blueprint(phieudatcho_bp)
    app.register_blueprint(vechuyenbay_bp)
    app.register_blueprint(HANHKHACH)
    app.register_blueprint(QUYDINH)

    app.scheduler = []

    with app.app_context():
        scheduler_flight = init_scheduler_flight(app)
        scheduler_paying = init_scheduler_paying(app)
        app.scheduler.extend([scheduler_flight, scheduler_paying])
    
    # @app.teardown_appcontext
    # def shutdow_scheduler(exception = None):
    #     for scheduler in app.scheduler:
    #         if scheduler.running:
    #             scheduler.shutdown()

    return app