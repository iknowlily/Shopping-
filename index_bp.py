from flask import Blueprint, render_template, request, session, redirect, jsonify
from models import db

index_bp = Blueprint("index_bp", __name__)
@index_bp.route('/')
def index():
    cid = request.args.get('cid')
    sql = 'SELECT * FROM category;'
    db.cursor.execute(sql)
    category1 = db.cursor.fetchmany(6)
    print(category1)
    if cid:
        sql = f'SELECT * FROM products where category_id={cid} order by ts_time desc;'
        db.cursor.execute(sql)
        product1 = db.cursor.fetchmany(5)
        sql1 = f'SELECT * FROM products where category_id={cid} order by ts_time desc limit 5,9;'
        db.cursor.execute(sql1)
        product2 = db.cursor.fetchmany(5)
        return render_template('index/index.html', product2=product2, product1=product1, category1=category1)
    sql1 = f'SELECT * FROM products where category_id={category1[0][0]} order by ts_time desc;'
    db.cursor.execute(sql1)
    product1 = db.cursor.fetchmany(5)
    sql3 = f'SELECT * FROM products where category_id={category1[0][0]} order by ts_time desc limit 5,9;'
    db.cursor.execute(sql3)
    product2 = db.cursor.fetchmany(5)
    return render_template('index/index.html', product2=product2, product1=product1, category1=category1)


@index_bp.route('/login')
def login():
    return render_template('login.html')

@index_bp.route('/get_user_logged_in')
# Returns information on the user's login status
def get_user_logged_in():
    user_logged_in = False
    if 'user_id' in session:
        user_logged_in = True
    return jsonify({'userLoggedIn': user_logged_in})

@index_bp.route('/register')
def register():
    return render_template('register.html')


@index_bp.route('/login_view', methods=['POST'])
def login_view():
    print(request.json)
    username = request.json.get('username')
    password = request.json.get('password')
    # Use the provided placeholder method to execute secure queries and prevent SQL injection
    sql = "SELECT * FROM user_ORM WHERE (username=%s OR email=%s OR phone_number=%s) AND password=%s"
    values = (username, username, username, password)
    db.cursor.execute(sql, values)
    user = db.cursor.fetchone()
    print(user)
    if user and user[-1] == 1:
        session['user_id'] = user[0]
        return jsonify({'status': 'admin', 'message': 'Login successful'})
    elif user:
        session['user_id'] = user[0]
        print(session)
        return jsonify({'status': 'success', 'message': 'Login successful'})
    else:
        return jsonify({'status': 'failed', 'message': 'Input error'})


@index_bp.route('/register', methods=['POST'])
def register_view():
    #Ensure that the requested Content Type is' application/json '.
    if request.headers['Content-Type'] != 'application/json':
        return jsonify({'status': 'failed', 'message': 'Invalid Content-Type'})
    #Use parameter binding to build SQL queries to avoid potential SQL injection issues
    data = request.get_json() #Obtain JSON data
    if not data:
        return jsonify({'status': 'failed', 'message': 'Invalid JSON data'})

    # cid = data.get('cid')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phonenumber')
    sex = data.get('sex')
    address = data.get('address')
    birthday = data.get('birthday')
    admin_id = data.get('admin_id')

    # Check whether the same username exists in the database
    sql = "SELECT * FROM user_ORM WHERE username = %s"
    values = (username,)
    db.cursor.execute(sql, values)
    existing_user = db.cursor.fetchone()

    if existing_user:
        # If the same username exists, a message that the user already exists is returned
        return jsonify({'status': 'failed', 'message': 'User already exists'})

    if admin_id == '1':
        sql = "INSERT INTO user_ORM (`username`, `password`, `sex`, `birthday`, `phone_number`, `email`, `address`, `admin_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        values = (username, password, sex, birthday, phone_number, email, address, admin_id)
        db.cursor.execute(sql, values)
        db.conn.commit()
        return jsonify({'status': 'success', 'message': 'User registered successfully'})

    sql = "INSERT INTO user_ORM (`username`, `password`, `sex`, `birthday`, `phone_number`, `email`, `address`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    values = (username, password, sex, birthday, phone_number, email, address)
    db.cursor.execute(sql, values)
    db.conn.commit()
    return jsonify({'status': 'success', 'message': 'User registered successfully'})

@index_bp.route('/logout', methods=['POST'])
def login_out():
    print(session)
    session.clear()
    print(session)
    return jsonify({'status': 'success', 'message': 'logout successfully'})

@index_bp.route('/search', methods=['POST'])
def search_products():
    category = request.json.get('category')

    # 根据不同的产品类别执行不同的数据库查询
    if category == 'category1':
        products = db.query_products_by_category1()
    elif category == 'category2':
        products = db.query_products_by_category2()
    elif category == 'category3':
        products = db.query_products_by_category3()
    elif category == 'category4':
        products = db.query_products_by_category4()
    elif category == 'category5':
        products = db.query_products_by_category5()
    elif category == 'category6':
        products = db.query_products_by_category6()
    else:
        return jsonify({'status': 'failed', 'message': 'Invalid category'})

    if products:
        return jsonify({'status': 'success', 'products': products})
    else:
        return jsonify({'status': 'failed', 'message': 'No products found for the given category'})
