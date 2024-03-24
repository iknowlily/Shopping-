from flask import Blueprint, render_template, request, session, redirect, jsonify

from com.user import required_login
from models import db

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route('/admin')
@required_login
def admin():
    user_id = session['user_id']
    sql1 = f"select * from user_ORM where id={user_id} and admin_id =1;"
    db.cursor.execute(sql1)
    user = db.cursor.fetchone()
    if user:
        sql = f"select * from products where user_id ={user_id} order by ts_time desc;"
        db.cursor.execute(sql)
        product = db.cursor.fetchall()
        print(f'product{product}')
        return render_template('admin/admin.html', product=product)
    return redirect('/')


@admin_bp.route('/admin_view/', methods=['POST'])
def admin_view():
    product = request.json.get('del_id')
    print(f'product{product}')
    sql = f"DELETE FROM products WHERE id={product};"
    db.cursor.execute(sql)
    db.conn.commit()
    return redirect('/admin')


@admin_bp.route('/admin_sure_view')
def admin_sure_view():
    user_id = session['user_id']
    sql = f'SELECT * from shopping_cart WHERE status="1"'
    sql2 = f'select count(*) from shopping_cart WHERE status="1"'
    db.cursor.execute(sql2)
    count = db.cursor.fetchall()
    # print(count)
    db.cursor.execute(sql)
    products = db.cursor.fetchall()
    # print(f'This is pro{products}')
    # products
    product = []
    users = []
    for i in products:
        sql1 = f'SELECT * FROM products WHERE id={i[1]} and user_id={user_id};'
        db.cursor.execute(sql1)
        product_ = db.cursor.fetchone()
        sql1 = f'SELECT * FROM user_ORM WHERE id={i[1]};'
        db.cursor.execute(sql1)
        user = db.cursor.fetchone()
        users.append(user)
        product.append(product_)
    return render_template('admin/product_sure.html', users=users, products=products, product=product, count=count)


@admin_bp.route('/admin_sure', methods=['POST'])
def admin_sure():
    print(request.json)
    cart_id = request.json.get('cart_id')
    sql = f"UPDATE shopping_cart SET status={1} WHERE id={int(cart_id)};"
    db.cursor.execute(sql)
    db.conn.commit()
    return jsonify({'status': 'success', 'message': 'successfully'})
