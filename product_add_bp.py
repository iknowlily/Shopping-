from flask import Blueprint, request, render_template, jsonify, session, redirect
from models import db
from com.user import required_login

product_add_bp = Blueprint('product_add_bp', __name__)


@product_add_bp.route('/product_add_view/')
def product_add_view():
    cid = request.args.get('product_id')
    if cid:
        sql = f"select * from products where id={cid};"
        db.cursor.execute(sql)
        product = db.cursor.fetchone()
        return render_template('admin/product_add.html',product=product)
    return render_template('admin/product_add.html')


@product_add_bp.route('/product_add', methods=['POST'])
@required_login
def product_add():
    print(request.json)
    merchant_name = request.json.get('merchant_name')
    category_id = request.json.get('category_id')
    products_name = request.json.get('products_name')
    cover = request.json.get('cover')
    price = request.json.get('price')
    content = request.json.get('content')
    merchant_address = request.json.get('merchant_address')
    status = 1
    user_id = session['user_id']
    new_price = request.json.get('new_price')
    duration = request.json.get('duration')
    promotion_reason = request.json.get('promotion_reason')
    if new_price:
        status = 0
    sql = f"insert into products (`category_id`,`user_id`, `products_name`,`merchant_name`, `price`,`merchant_address`, `cover`,`content`,`new_price`, `duration`,`promotion_reason`,`status`) values ('{category_id}','{user_id}','{products_name}','{merchant_name}','{price}','{merchant_address}','{cover}','{content}','{new_price}','{duration}','{promotion_reason}','{status}')"
    db.cursor.execute(sql)
    db.conn.commit()
    return jsonify({'status': 'success', 'message': 'Add successfully'})
