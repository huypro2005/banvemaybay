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
import os



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
    return app