from flask import Flask

from .index_bp import index_bp
from .product_bp import product_bp
from .search_bp import search_bp
from .user_bp import user_bp
from .admin_bp import admin_bp
from .product_add_bp import product_add_bp


def register_blueprint(app: Flask):
    app.config['SECRET_KEY'] = '123456789'
    app.register_blueprint(index_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(product_add_bp)
    app.register_blueprint(user_bp)
