from flask import Blueprint, request, render_template, g, jsonify, session
from models import db

search_bp = Blueprint('search_bp', __name__)


@search_bp.route('/shopping_cart')
def shopping_cart():
    cid = request.args.get('cid')
    user_id = session['user_id']
    sql = f'SELECT * FROM shopping_cart WHERE status="0" and user_id={user_id};'
    sql2 = f'select count(*) from shopping_cart WHERE status="0" and user_id={user_id};'
    db.cursor.execute(sql2)
    count = db.cursor.fetchall()
    print(count)
    db.cursor.execute(sql)
    products = db.cursor.fetchall()
    print(f'This is pro{products}')
    # product
    product = []
    for i in products:
        sql1 = f'SELECT * FROM products WHERE id={i[1]};'
        db.cursor.execute(sql1)
        product_ = db.cursor.fetchone()
        print(product_)
        product.append(product_)
    if cid:
        sql2 = f"UPDATE shopping_cart SET status={3} WHERE id={cid} and user_id={user_id};"
        db.cursor.execute(sql2)
        db.conn.commit()
    print(f'index{product}')
    return render_template('user/shopping_cart.html', products=products, product=product, count=count)


@search_bp.route('/cart', methods=['POST'])
def cart():
    products = request.json.get('product')
    user_id = session['user_id']
    print(products)

    if not products:  # Check whether products is an empty list
        return jsonify({'status': 'error', 'message': 'No products selected.'})

    selected_products = []  # Store the selected products

    if products[0] == 'on':
        if len(products) > 1:
            for i in range(1, len(products)):
                selected_products.append(int(products[i]))

    else:
        for product_id in products:
            selected_products.append(int(product_id))

    if not selected_products:  # Check that the list of selected items is empty
        return jsonify({'status': 'error', 'message': 'No products selected.'})

    for product_id in selected_products:
        sql1 = f"UPDATE shopping_cart SET status={-1} WHERE product_id={product_id} and user_id={user_id};"
        db.cursor.execute(sql1)
        print(db.cursor.execute(sql1))
        db.conn.commit()
        print('Buy')

    return jsonify({'status': 'success'})
