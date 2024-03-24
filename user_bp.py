from flask import Blueprint, render_template, request, session, redirect, jsonify

from com.user import required_login
from models import db

user_bp = Blueprint("user_bp", __name__)
@user_bp.route('/user_cart')
@required_login
def user_cart():
    user_id = session['user_id']
    sql = f'SELECT * FROM shopping_cart WHERE user_id={user_id};'
    sql2 = f'select count(*) from shopping_cart WHERE user_id={user_id};'
    db.cursor.execute(sql2)
    count = db.cursor.fetchall()
    # print(count)
    db.cursor.execute(sql)
    # shopping cart
    products = db.cursor.fetchall()
    # print(f'This  is pro{products}')
    # product
    product = []
    for i in products:
        sql1 = f'SELECT * FROM products WHERE id={i[1]};'
        db.cursor.execute(sql1)
        product_ = db.cursor.fetchone()
        # print(product_)
        product.append(product_)
    # print(f'index{product}')
    return render_template('user/user.html', products=products, product=product, count=count)


