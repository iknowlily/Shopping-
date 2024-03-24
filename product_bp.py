from datetime import datetime

from flask import Blueprint, render_template, request, g, jsonify, session
from models import db
from com.user import required_login

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/products/<int:product_id>')
def get_product(product_id):
    sql = f"select * from products where id={product_id};"
    db.cursor.execute(sql)
    product = db.cursor.fetchone()
    sql1 = f"select * from comment where product_id = {product[0]};"
    sq3 = f"select count(*) from comment where product_id = {product[0]};"
    db.cursor.execute(sq3)
    count = db.cursor.fetchall()
    db.cursor.execute(sql1)
    comment_list = db.cursor.fetchall()
    user_list = []
    # print(comment_list)
    for i in comment_list:
        # print(f'comm:{i}')
        # print(i[2])
        sql2 = f"select * from user_ORM where id = {i[2]};"
        db.cursor.execute(sql2)
        user = db.cursor.fetchone()
        user_list.append(user)
    # print(product)
    return render_template('index/product.html', product=product, comment_list=comment_list, user_list=user_list,
                           count=count)


@product_bp.route('/products/comment', methods=['POST'])
@required_login
def get_comment():
    product_id = request.json.get('product_id')
    content = request.json.get('content')
    user_id = session['user_id']
    print(request.json)
    comment_time = datetime.now()
    sql = f"insert into comment (`product_id`, `user_id`, `content`, `create_time`) values ('{product_id}', '{user_id}', '{content}', '{comment_time}');"
    db.cursor.execute(sql)
    db.conn.commit()
    return jsonify({'status': 'success', 'message': 'comment successfully'})

@product_bp.route('/products/like', methods=['POST'])
@required_login
def products_like():
    print(f'{request.json}request.json')
    product_id = request.json.get('product_id')
    cont = request.json.get('cont')
    content = ['like', 'unlike']
    sql1 = f"select * from products where id = {product_id};"
    db.cursor.execute(sql1)
    product = db.cursor.fetchone()
    print(product)
    user_id = session['user_id']
    if cont in content:
        if cont == 'like':
            sql = f"UPDATE products SET  likes='{product[-3] + 1}' WHERE id='{int(product_id)}';"
        else:
            sql = f"UPDATE products SET not_likes='{product[-2] + 1}' WHERE id='{int(product_id)}';"
        db.cursor.execute(sql)
        db.conn.commit()
        return jsonify({'status': 'successful', 'message': f'{cont} successful!'})
    return jsonify({'status': 'failed', 'message': 'data exception'})

@product_bp.route('/product/cart', methods=['POST'])
@required_login
def product_cart():
    print(request.json)
    cart_id = request.json.get('cart_id')
    status = request.json.get('status')
    count = request.json.get('count')
    # return a list
    product_id = request.json.get('product_id')
    user_id = session['user_id']
    if cart_id:
        sql = f"UPDATE shopping_cart SET status={3} WHERE id={int(cart_id)};"
        db.cursor.execute(sql)
        db.conn.commit()
        print('emm')
        return jsonify({'status': 'success', 'message': 'successfully'})
    if status == -1:
        sql = f"insert into shopping_cart (`product_id`,`user_id`, `count`, `status`) values ('{product_id}', '{user_id}', '{count}', '{status}');"
        db.cursor.execute(sql)
        db.conn.commit()
        print('mail')
        return jsonify({'status': 'success', 'message': 'pay success', 'code': status})
    if status == 0:
        sql1 = f"insert into shopping_cart (`product_id`,`user_id`, `count`, `status`) values ('{product_id}', '{user_id}', '{count}', '{status}');"
        db.cursor.execute(sql1)
        db.conn.commit()
        print('aaa')
        return jsonify({'status': 'success', 'message': 'add shopping_cart success', 'code': status})
