from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from flask_pymongo import PyMongo, MongoClient
from pymongo import MongoClient
from insert_in_mongo import insert

app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bhavin@123',
    'database': 'grocery_store'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


client = MongoClient('mongodb://localhost:27017/')
db = client['food_delivery']  # Replace 'your_database' with your actual database name
collection = db['g_data']
user = db['users']
cart_collection = db['cart']
total_collection = db['total_info']
orders=db['order']
admin=db['admin']

# insert()
# MongoDB Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/food_delivery'
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/index')
def ind():
    return render_template('index.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # if request.method == 'POST':
    #     # Fetch form data
    #     senddata = request.form
    #     return render_template('cart.html', groceries=senddata)
    # Fetch all items from the cart
    calculate_total_price_and_save()
    groce = cart_collection.find({})
    total_price=total_collection.find({})
    return render_template('cart.html', groceries=groce,total_price=total_price)


@app.route('/fruit', methods=['GET', 'POST'])
def fruit():
    if request.method == 'POST':
        # Fetch form data
        senddata = request.form
        return render_template('cart.html', groceries=senddata)

    groceries = collection.find({})
    return render_template('fruit.html', groceries=groceries)


def getCartDetails():
    pro = cart_collection.find()

    if pro:
        # Return the product details if found
        return {
            "name": pro["name"],
            "description": pro["description"],
            "price": pro["price"],

            "image_url": pro["image_url"]
            # Add more fields as needed
        }
    else:
        # Return None if product not found
        return None


@app.route('/cartActivity', methods=['GET', 'POST'])
def open_cart():
    product_details = cart_collection.find()
    return render_template('cartActivity.html', groceries=product_details)


def getProductDetails(product_name):
    # Query MongoDB to find the product with the given name
    product = collection.find_one({"name": product_name})

    if product:
        # Return the product details if found
        return {
            "name": product["name"],
            "description": product["description"],
            "price": product["price"],

            "image_url": product["image_url"]
            # Add more fields as needed
        }
        ksdjf={"description": product["description"]}
    else:
        # Return None if product not found
        return None


@app.route('/add_to_cart/<product_name>')
def add_to_cart(product_name):
    # product_details = getCartDetails(product_name)

    cartcolle = mongo.db.cart

    prod = collection.find_one({"name": product_name})

    if prod:
        # Return the product details if found
        a = {
            "name": prod["name"],
            "description": prod["description"],
            "price": prod["price"],
            "dicount": prod["dicount"],
            "image_url": prod["image_url"],
            "quantity": prod["quantity"]
            # Add more fields as needed
        }
    else:
        # Return None
        # if product not found
        return None

    cartcolle.insert_one(a)
    return render_template('popup.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/buyNow', methods=['GET','POST'])
def buyNow():
    groce = cart_collection.find({})
    total_price = total_collection.find({})
    return render_template('buyNow.html', groceries=groce, total_price=total_price)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        password = userDetails['password']

        # Save user data to MySQL
        conn = get_db_connection()
        cur = conn.cursor()
        # cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, password) VALUES(%s, %s, %s)", (name, email, password))
        conn.commit()
        cur.close()
        conn.close()

        # Save user data to MongoDB
        users = mongo.db.users
        users.insert_one({'name': name, 'email': email, 'password': password})

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin_panel', methods=['GET','POST'])
def admin_panel():
    deliveries = admin.find({})
    return render_template('admin_panel.html',deliveries=deliveries)
@app.route('/delivery_dtail',methods=['POST'])
def delivery_dtail():
    username = request.form.get('username')
    address = request.form.get('address')
    phone = request.form.get('phone')
    payment_method = request.form.get('payment_method')
    # Insert the delivery and payment details into the database
    admin.insert_one({
        'username': username,
        'address': address,
        'phone': phone,
        'payment':payment_method

    })

    return "Your order is Placed!"
@app.route('/place_order', methods=['POST'])
def place_order():
    # Get the total price from the request data
    total_price = request.form['total_price']

    # Create a new order document in MongoDB
    order = {
        'total_price': total_price,
        'created_at': datetime.utcnow()
    }
    orders.insert_one(order)

    # Redirect the user to the order confirmation page
    return render_template('delivery_detail.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        email = userDetails['email']
        password = userDetails['password']
        # Check user credentials from MySQL
        conn = get_db_connection()
        cur = conn.cursor()
        result = cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))

        if result:
            # User exists, set session variables
            session['loggedin'] = True
            session['email'] = email
            session['password'] = password
            return render_template('home.html')
        else:
            return render_template('home.html')
    return render_template('login.html')

@app.route('/update_quantity/<product_id>/<quentity>', methods=['GET','POST'])
def update_quantity(product_id, quentity):
    # Find the product in the cart by its ID
    product = cart_collection.find_one({"name": product_id})
    if product:
        # Update the quantity
        if quentity == 1:
            quentity+=1
            total_collection.update_one({}, {"$set": {"$sum": {"quantity": "$quentity" + 1}}})

        elif quentity == -1:
            quentity-=1
            total_collection.update_one({}, {"$set": {"$subtract": {"quantity": "$quentity" - 1}}})


        return
    else:
        return jsonify({"success": False, "message": "Product not found"}), 404


def calculate_total_price_and_save():
    # Fetch all items from the cart
    items = list(cart_collection.find({}))

    # Calculate total price
    total_price = sum(item['price'] for item in items)

    # Create a new dictionary with the total price and other information
    total_info = {
        "total_price": total_price,
        "items_count": len(items),
        "items": items  # Include all items for reference
    }

    # Save the total info to MongoDB

    total_collection.update_one({}, {"$set": {"total_price": total_price, "items_count": len(items), "items": items}})

if __name__ == '__main__':
    app.run(debug=True)
